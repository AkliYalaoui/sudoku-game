import streamlit as st
from src.core import ColorSudoku

def main():
    st.title("Sudoku des Couleurs")

    # Select grid rank
    rank = st.selectbox("Select Grid Rank", [2, 3, 4], index=1)
    size = rank ** 2  # Sudoku size

    height,width = 40, 47
    if size == 16:
        height,width = 40, 27
    elif size == 4:
        height,width = 40, 130

    if "game" not in st.session_state or st.session_state.game.size != size:
        st.session_state.game = ColorSudoku(size=size)

    game = st.session_state.game

    # Dropdown to select algorithm
    algorithm = st.selectbox("Select Sudoku Generation Algorithm", ["Backtracking", "MRV", "Dsatur", "Knuth"])

    if st.button("Generate New Puzzle"):
        st.session_state.game = ColorSudoku(size=size, algorithm=algorithm)
        st.rerun()

    st.write("Sélectionnez une couleur et cliquez sur une case pour colorier.")
    
    col1, col2 = st.columns([4, 1])
    
    with col2:
        selected_color = st.radio("Couleur sélectionnée", game.colors, index=0, key="color_selector")
    
    with col1:
        for r in range(game.size):
            cols = st.columns(game.size)
            for c in range(game.size):
                color = game.grid[r][c]
                cell_style = f"width:{width}px; height:{height}px;"

                if color is None:
                    if cols[c].button(" ", key=f"{r}-{c}", help=f"Choisir cette case ({r+1},{c+1})", use_container_width=True):
                        game.set_user_color(r, c, selected_color)
                        st.rerun()
                else:
                    cols[c].markdown(
                        f'<div style="border-radius:5px; display:flex; align-items:center; justify-content:center; border:1px solid #999; {cell_style} background-color:{color};"></div>',
                        unsafe_allow_html=True
                    )

    st.markdown("---")
    col3, col4, col5 = st.columns(3)
    with col3:
        if st.button("Vérifier la solution"):
            if game.is_valid_solution():
                st.success("Bravo ! Votre solution respecte les règles du Sudoku !")
            else:
                st.error("Il y a des erreurs dans votre solution.")
    with col4:
        if st.button("Afficher la solution"):
            game.reveal_solution()
            st.rerun()
    with col5:
        if st.button("Recommencer"):
            st.session_state.game = ColorSudoku(size=size, algorithm=algorithm)
            st.rerun()

if __name__ == "__main__":
    main()