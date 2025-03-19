# Importation des bibliothèques nécessaires
import streamlit as st  # Streamlit pour la création de l'application web interactive.
from src.core import ColorSudoku  # Importation de la classe ColorSudoku, qui est responsable de la génération et de la gestion du Sudoku des couleurs.

# Fonction principale qui est exécutée lors de l'appel de l'application Streamlit.
def main():
    st.title("Sudoku des Couleurs")  # Affichage du titre de l'application.

    # Sélection de la "rank" (le rang) de la grille, ici on permet de choisir entre des tailles 2x2, 3x3 ou 4x4 (qui donneront des grilles de 4x4, 9x9, 16x16).
    rank = st.selectbox("Select Grid Rank", [2, 3, 4], index=1)  # Par défaut, on choisit 3 (grille 9x9).
    size = rank ** 2  # Calcul de la taille totale du Sudoku (par exemple, si rank=3, size = 9).

    # Définition de la hauteur et de la largeur des cellules de la grille selon la taille du Sudoku.
    height, width = 40, 47  # Par défaut, on définit une taille de cellule pour une grille de 9x9.
    if size == 16:  # Si la grille est 16x16, on réduit la largeur des cellules.
        height, width = 40, 27
    elif size == 4:  # Si la grille est 4x4, on augmente la largeur des cellules.
        height, width = 40, 130

    # Vérification si la session contient déjà un jeu. Si ce n'est pas le cas ou si la taille a changé, on crée un nouveau jeu.
    if "game" not in st.session_state or st.session_state.game.size != size:
        st.session_state.game = ColorSudoku(size=size)  # Création d'un nouveau jeu de Sudoku des couleurs avec la taille définie.

    game = st.session_state.game  # On récupère l'objet 'game' de la session.

    # Dropdown pour choisir l'algorithme de génération du Sudoku.
    algorithm = st.selectbox("Select Sudoku Generation Algorithm", ["Backtracking", "MRV", "Dsatur", "Knuth"])

    # Bouton pour générer un nouveau puzzle.
    if st.button("Generate New Puzzle"):
        st.session_state.game = ColorSudoku(size=size, algorithm=algorithm)  # Génération d'un nouveau Sudoku avec l'algorithme choisi.
        st.rerun()  # Redémarre l'application pour recharger le puzzle généré.

    # Instructions pour l'utilisateur pour sélectionner une couleur et remplir la grille.
    st.write("Sélectionnez une couleur et cliquez sur une case pour colorier.")
    
    col1, col2 = st.columns([4, 1])  # Crée deux colonnes dans l'interface utilisateur (une large et une étroite).

    # Colonne pour choisir une couleur.
    with col2:
        selected_color = st.radio("Couleur sélectionnée", game.colors, index=0, key="color_selector")  # Permet à l'utilisateur de choisir une couleur parmi les couleurs disponibles.

    # Colonne principale pour afficher la grille et permettre à l'utilisateur de colorier les cases.
    with col1:
        for r in range(game.size):  # Parcourt toutes les lignes de la grille.
            cols = st.columns(game.size)  # Crée des colonnes dans Streamlit pour chaque cellule de la ligne.
            for c in range(game.size):  # Parcourt chaque cellule de la ligne.
                color = game.grid[r][c]  # Récupère la couleur de la case (ou None si elle est vide).
                cell_style = f"width:{width}px; height:{height}px;"  # Définition du style CSS pour chaque cellule.

                if color is None:  # Si la case est vide (pas encore coloriée).
                    # Crée un bouton pour colorier la case (lorsque l'utilisateur clique dessus).
                    if cols[c].button(" ", key=f"{r}-{c}", help=f"Choisir cette case ({r+1},{c+1})", use_container_width=True):
                        game.set_user_color(r, c, selected_color)  # Applique la couleur sélectionnée à la case.
                        st.rerun()  # Redémarre l'application pour mettre à jour la grille après chaque action.
                else:  # Si la case est déjà coloriée.
                    # Affiche la couleur de la case.
                    cols[c].markdown(
                        f'<div style="border-radius:5px; display:flex; align-items:center; justify-content:center; border:1px solid #999; {cell_style} background-color:{color};"></div>',
                        unsafe_allow_html=True  # Utilise HTML et CSS pour afficher la cellule coloriée.
                    )

    # Séparateur visuel entre la grille et les boutons d'action.
    st.markdown("---")

    # Crée trois colonnes pour afficher des boutons d'actions.
    col3, col4, col5 = st.columns(3)
    with col3:
        if st.button("Vérifier la solution"):  # Bouton pour vérifier si la solution est correcte.
            if game.is_valid_solution():  # Vérifie si la grille respecte les règles du Sudoku des couleurs.
                st.success("Bravo ! Votre solution respecte les règles du Sudoku !")  # Affiche un message de succès si la solution est correcte.
            else:
                st.error("Il y a des erreurs dans votre solution.")  # Affiche un message d'erreur si la solution n'est pas valide.
    with col4:
        if st.button("Afficher la solution"):  # Bouton pour afficher la solution du puzzle.
            game.reveal_solution()  # Révèle la solution du puzzle (remet les couleurs dans les cases).
            st.rerun()  # Redémarre l'application pour afficher la grille avec la solution.
    with col5:
        if st.button("Recommencer"):  # Bouton pour recommencer une nouvelle partie.
            st.session_state.game = ColorSudoku(size=size, algorithm=algorithm)  # Crée un nouveau jeu de Sudoku des couleurs avec la même taille et le même algorithme.
            st.rerun()  # Redémarre l'application pour recommencer le jeu.

# Appelle la fonction main si ce script est exécuté en tant qu'application Streamlit.
if __name__ == "__main__":
    main()
