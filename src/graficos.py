import matplotlib
import matplotlib.pyplot as plt
import numpy as np


matplotlib.use('Agg')  # obligatorio para entornos sin pantalla


def histograma(datos: list, titulo: str, ruta: str) -> None:
    """Genera histograma con 10 bins y línea de media. Guarda en ruta."""
    arr = np.array(datos, dtype=float)
    media = float(np.mean(arr))

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(arr, bins=10, color="#4C9BE8", edgecolor="white", alpha=0.85)
    ax.axvline(media, color="#E84C4C", linewidth=2, linestyle="--",
               label=f"Media: {media:.2f}")
    ax.set_title(titulo, fontsize=14, fontweight="bold")
    ax.set_xlabel("Valor")
    ax.set_ylabel("Frecuencia")
    ax.legend()
    fig.tight_layout()
    fig.savefig(ruta, dpi=100)
    plt.close(fig)


def boxplot_comparativo(datos_a: list, datos_b: list,
                        etiquetas: list, ruta: str) -> None:
    """Genera boxplot comparativo de dos series. Guarda en ruta."""
    fig, ax = plt.subplots(figsize=(7, 5))
    bp = ax.boxplot(
        [datos_a, datos_b],
        tick_labels=etiquetas,
        patch_artist=True,
        medianprops=dict(color="white", linewidth=2),
    )
    colores = ["#4C9BE8", "#E84C4C"]
    for patch, color in zip(bp["boxes"], colores):
        patch.set_facecolor(color)
        patch.set_alpha(0.75)
    ax.set_title("Boxplot Comparativo", fontsize=14, fontweight="bold")
    ax.set_ylabel("Valor")
    fig.tight_layout()
    fig.savefig(ruta, dpi=100)
    plt.close(fig)