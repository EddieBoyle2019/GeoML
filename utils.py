# Utilities required for Sentinel Hub API
# Eddie Boyle Sep 2023

from typing import Any, Optional, Tuple

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def plot_image(
    image: np.ndarray,
    factor: float = 1.0,
    clip_range: Optional[Tuple[float, float]] = None,
    **kwargs: Any
) -> None:
    # Utility function for plotting RGB images
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 15))
    if clip_range is not None:
        ax.imshow(np.clip(image * factor, *clip_range), **kwargs)
    else:
        ax.imshow(image * factor, **kwargs)
    ax.set_xticks([])
    ax.set_yticks([])

    # Required for Streamlit
    st.pyplot(fig)