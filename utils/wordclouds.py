import io
import numpy as np
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

def get_mask(path="assets/star_mask.png"):
    """Load mask image from path."""
    if path and os.path.exists(path):
        return np.array(Image.open(path))
    return None

def get_font(path="assets/PlayfairDisplay.ttf"):
    """Load font path if exists."""
    if path and os.path.exists(path):
        return path
    return None

def generate_words(df: pd.DataFrame):
    """Extract and combine words from submission DataFrame."""
    return " ".join(df["response1"].fillna("").tolist() + df["response2"].fillna("").tolist())

def render_wordcloud(words, font_path=None, mask=None, colormap="viridis"):
    """Generate word cloud image and buffer."""
    wc = WordCloud(
        width=800,
        height=400,
        background_color="white",
        font_path=font_path,
        mask=mask,
        colormap=colormap
    ).generate(words)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")

    buf = io.BytesIO()
    wc.to_image().save(buf, format="PNG")
    buf.seek(0)

    return fig, buf