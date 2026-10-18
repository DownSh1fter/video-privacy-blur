"""Streamlit interface for the local video anonymization baseline."""

from __future__ import annotations

import tempfile
from pathlib import Path

import streamlit as st

from privacy_blur.video import process_video


st.set_page_config(page_title="Video Privacy Blur", page_icon="🔒", layout="wide")
st.title("Video Privacy Blur")
st.write(
    "Загрузите короткое видео: baseline попробует найти лица и номерные знаки, "
    "размыть их и подготовить видео для скачивания."
)
st.warning(
    "Это первая версия на Haar Cascade. Она может пропускать объекты и не подходит "
    "для гарантированного обезличивания. Видеофайл обрабатывается локально; звук "
    "в выходном файле пока не сохраняется."
)

uploaded = st.file_uploader(
    "Выберите видео",
    type=["mp4", "avi", "mov", "mkv"],
    help="Для первого запуска лучше использовать короткий файл с несколькими лицами или автомобилями.",
)

if uploaded is not None:
    st.video(uploaded)
    if st.button("Обработать видео", type="primary"):
        progress = st.progress(0.0, text="Подготовка…")
        try:
            with tempfile.TemporaryDirectory(prefix="video-privacy-blur-") as temp_dir:
                source_path = Path(temp_dir) / f"input{Path(uploaded.name).suffix.lower()}"
                output_path = Path(temp_dir) / "anonymized.mp4"
                source_path.write_bytes(uploaded.getvalue())
                stats = process_video(
                    source_path,
                    output_path,
                    progress=lambda fraction: progress.progress(
                        fraction,
                        text=f"Обработано: {fraction:.0%}",
                    ),
                )
                result_bytes = output_path.read_bytes()

            st.success(
                f"Готово: {stats.frames} кадров за {stats.elapsed_seconds:.1f} с "
                f"({stats.processing_fps:.1f} FPS; исходное видео — {stats.source_fps:.1f} FPS)."
            )
            st.video(result_bytes)
            st.download_button(
                "Скачать обезличенное видео",
                data=result_bytes,
                file_name=f"{Path(uploaded.name).stem}_anonymized.mp4",
                mime="video/mp4",
            )
            st.caption(
                "Обязательно просмотрите результат: baseline может пропустить лицо или номер. "
                "В выходном MP4 нет звуковой дорожки."
            )
        except Exception as error:  # Display readable errors in the learning UI.
            st.error(f"Не удалось обработать видео: {error}")
