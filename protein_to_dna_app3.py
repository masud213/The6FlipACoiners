from dash import Dash, html, dcc, Input, Output, State

# Most frequent codon for each amino acid (from the CDS-based E. coli counts)
most_frequent_codon = {
    "F": "TTT", "L": "CTG", "I": "ATT", "M": "ATG", "V": "GTG",
    "S": "AGC", "P": "CCG", "T": "ACC", "A": "GCG", "Y": "TAT",
    "H": "CAT", "Q": "CAG", "N": "AAC", "K": "AAA", "D": "GAT",
    "E": "GAA", "C": "TGC", "W": "TGG", "R": "CGC", "G": "GGC",
    "STOP": "TAA",
}

# Amino acid names and their one-letter codes (for the side table)
amino_acid_names = {
    "A": "Alanine", "R": "Arginine", "N": "Asparagine", "D": "Aspartic acid",
    "C": "Cysteine", "Q": "Glutamine", "E": "Glutamic acid", "G": "Glycine",
    "H": "Histidine", "I": "Isoleucine", "L": "Leucine", "K": "Lysine",
    "M": "Methionine", "F": "Phenylalanine", "P": "Proline", "S": "Serine",
    "T": "Threonine", "W": "Tryptophan", "Y": "Tyrosine", "V": "Valine",
}

example_protein = (
    "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAED\n"
    "LQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN"
)


def protein_to_dna(protein, add_stop=True):
    """Convert a protein string to DNA using the most frequent codon for each amino acid."""
    # Remove line breaks and spaces, make uppercase
    protein = "".join(protein.split()).upper()

    dna = ""
    for amino_acid in protein:
        if amino_acid not in most_frequent_codon or amino_acid == "STOP":
            return None, f"'{amino_acid}' is not a valid amino acid letter."
        dna += most_frequent_codon[amino_acid]

    if add_stop:
        dna += most_frequent_codon["STOP"]

    return dna, None


def make_amino_acid_table():
    """Build an HTML table of amino acid names and one-letter codes."""
    cell = {"border": "1px solid #ccc", "padding": "4px 10px"}
    header = html.Tr([html.Th("Amino acid", style=cell), html.Th("Code", style=cell)])
    rows = [
        html.Tr([html.Td(name, style=cell),
                 html.Td(letter, style={**cell, "textAlign": "center", "fontWeight": "bold"})])
        for letter, name in sorted(amino_acid_names.items(), key=lambda item: item[1])
    ]
    return html.Table([header] + rows, style={"borderCollapse": "collapse"})


app = Dash(__name__)

card_style = {
    "background": "rgba(255, 255, 255, 0.93)",
    "padding": "20px",
    "borderRadius": "10px",
    "boxShadow": "0 2px 8px rgba(0,0,0,0.3)",
}

app.layout = html.Div(
    style={"minHeight": "100vh", "fontFamily": "sans-serif"},
    children=[
        # Header bar with the coin logo in the top left
        html.Div(
            style={"display": "flex", "alignItems": "center", "gap": "15px",
                   "padding": "10px 20px", "background": "rgba(0, 0, 0, 0.65)",
                   "color": "white"},
            children=[
                html.Img(src=app.get_asset_url("logo.png"),
                         style={"height": "60px", "width": "60px"}),
                html.H2("Protein to DNA converter", style={"margin": "0"}),
            ],
        ),
        # Page content
        html.Div(
            style={"maxWidth": "1100px", "margin": "30px auto", "padding": "0 20px",
                   "display": "flex", "gap": "30px", "alignItems": "flex-start"},
            children=[
                # Main column
                html.Div(
                    style={**card_style, "flex": "1", "minWidth": "0"},
                    children=[
                        html.P("Paste a protein sequence (one-letter codes). Each amino acid "
                               "is converted to its most frequent E. coli codon."),
                        dcc.Textarea(
                            id="protein-input",
                            value=example_protein,
                            style={"width": "100%", "height": "120px", "fontFamily": "monospace"},
                        ),
                        dcc.Checklist(
                            id="stop-option",
                            options=[{"label": " Add stop codon (TAA) at the end", "value": "stop"}],
                            value=["stop"],
                            style={"margin": "10px 0"},
                        ),
                        html.Button("Convert", id="convert-button", n_clicks=0),
                        html.Div(id="summary", style={"marginTop": "20px", "fontWeight": "bold"}),
                        html.Pre(
                            id="dna-output",
                            style={"whiteSpace": "pre-wrap", "wordBreak": "break-all",
                                   "background": "#f4f4f4", "padding": "10px", "marginTop": "10px"},
                        ),
                    ],
                ),
                # Side column: amino acid reference table
                html.Div(
                    style={**card_style, "flex": "none"},
                    children=[
                        html.H3("Amino acid codes", style={"marginTop": "0"}),
                        make_amino_acid_table(),
                    ],
                ),
            ],
        ),
    ],
)


@app.callback(
    Output("dna-output", "children"),
    Output("summary", "children"),
    Input("convert-button", "n_clicks"),
    State("protein-input", "value"),
    State("stop-option", "value"),
)
def convert(n_clicks, protein, stop_option):
    if not protein or not protein.strip():
        return "", "Please enter a protein sequence."

    dna, error = protein_to_dna(protein, add_stop="stop" in stop_option)
    if error:
        return "", error

    n_aa = len("".join(protein.split()))
    return dna, f"{n_aa} amino acids -> {len(dna)} bases"


if __name__ == "__main__":
    app.run(debug=True)
