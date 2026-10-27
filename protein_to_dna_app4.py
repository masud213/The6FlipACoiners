from dash import Dash, html, dcc, Input, Output, State, ALL, ctx, no_update
from dash.exceptions import PreventUpdate

# Most frequent codon for each amino acid (from the CDS-based E. coli counts)
most_frequent_codon = {
    "F": "TTT", "L": "CTG", "I": "ATT", "M": "ATG", "V": "GTG",
    "S": "AGC", "P": "CCG", "T": "ACC", "A": "GCG", "Y": "TAT",
    "H": "CAT", "Q": "CAG", "N": "AAC", "K": "AAA", "D": "GAT",
    "E": "GAA", "C": "TGC", "W": "TGG", "R": "CGC", "G": "GGC",
    "STOP": "TAA",
}

# One-letter code -> (amino acid name, three-letter code), used by the side table
amino_acids = {
    "A": ("Alanine", "Ala"), "R": ("Arginine", "Arg"), "N": ("Asparagine", "Asn"),
    "D": ("Aspartic acid", "Asp"), "C": ("Cysteine", "Cys"), "Q": ("Glutamine", "Gln"),
    "E": ("Glutamic acid", "Glu"), "G": ("Glycine", "Gly"), "H": ("Histidine", "His"),
    "I": ("Isoleucine", "Ile"), "L": ("Leucine", "Leu"), "K": ("Lysine", "Lys"),
    "M": ("Methionine", "Met"), "F": ("Phenylalanine", "Phe"), "P": ("Proline", "Pro"),
    "S": ("Serine", "Ser"), "T": ("Threonine", "Thr"), "W": ("Tryptophan", "Trp"),
    "Y": ("Tyrosine", "Tyr"), "V": ("Valine", "Val"),
}

# Well-known proteins for the example buttons
examples = {
    "Insulin": {
        "info": "Human preproinsulin (110 amino acids)",
        "sequence": "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAEDLQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN",
    },
    "GFP": {
        "info": "Green fluorescent protein from the jellyfish Aequorea victoria (238 amino acids)",
        "sequence": "MSKGEELFTGVVPILVELDGDVNGHKFSVSGEGEGDATYGKLTLKFICTTGKLPVPWPTLVTTFSYGVQCFSRYPDHMKQHDFFKSAMPEGYVQERTIFFKDDGNYKTRAEVKFEGDTLVNRIELKGIDFKEDGNILGHKLEYNYNSHNVYIMADKQKNGIKVNFKIRHNIEDGSVQLADHYQQNTPIGDGPVLLPDNHYLSTQSALSKDPNEKRDHMVLLEFVTAAGITHGMDELYK",
    },
    "Lysozyme": {
        "info": "Hen egg-white lysozyme (129 amino acids)",
        "sequence": "KVFGRCELAAAMKRHGLDNYRGYSLGNWVCAAKFESNFNTQATNRNTDGSTDYGILQINSRWWCNDGRTPGSRNLCNIPCSALLSSDITASVNCAKKIVSDGNGMNAWVAWRNRCKGTDVQAWIRGCRL",
    },
    "Ubiquitin": {
        "info": "Human ubiquitin (76 amino acids)",
        "sequence": "MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG",
    },
    "Glucagon": {
        "info": "Human glucagon (29 amino acids)",
        "sequence": "HSQGTFTSDYSKYLDSRRAQDFVQWLMNT",
    },
}

example_protein = examples["Insulin"]["sequence"]


def protein_to_dna(protein, add_stop=True):
    """Convert a protein string to DNA using the most frequent codon for each amino acid."""
    # Remove line breaks and spaces, make uppercase
    protein = "".join(protein.split()).upper()

    dna = ""
    for amino_acid in protein:
        if amino_acid not in amino_acids:
            return None, f"'{amino_acid}' is not a valid amino acid letter."
        dna += most_frequent_codon[amino_acid]

    if add_stop:
        dna += most_frequent_codon["STOP"]

    return dna, None


def make_amino_acid_table(search=""):
    """Build an HTML table of amino acids, filtered by the search text."""
    query = (search or "").strip().lower()
    cell = {"border": "1px solid #ccc", "padding": "4px 10px"}
    centre = {**cell, "textAlign": "center"}

    header = html.Tr([
        html.Th("Amino acid", style=cell),
        html.Th("3-letter", style=cell),
        html.Th("1-letter", style=cell),
    ])

    rows = []
    for letter, (name, three) in sorted(amino_acids.items(), key=lambda item: item[1][0]):
        # Match the name, the 3-letter code, or the exact 1-letter code
        if query and not (query in name.lower() or query in three.lower() or query == letter.lower()):
            continue
        rows.append(html.Tr([
            html.Td(name, style=cell),
            html.Td(three, style=centre),
            html.Td(letter, style={**centre, "fontWeight": "bold"}),
        ]))

    if not rows:
        return html.P("No matching amino acids.", style={"color": "#666"})

    return html.Table([header] + rows, style={"borderCollapse": "collapse"})


app = Dash(__name__)

card_style = {
    "background": "rgba(255, 255, 255, 0.93)",
    "padding": "20px",
    "borderRadius": "10px",
    "boxShadow": "0 2px 8px rgba(0,0,0,0.3)",
}

button_style = {"padding": "6px 14px", "marginRight": "8px", "marginTop": "6px", "cursor": "pointer"}

app.layout = html.Div(
    style={"minHeight": "100vh", "fontFamily": "sans-serif"},
    children=[
        # Header bar: coin logo and team name
        html.Div(
            style={"display": "flex", "alignItems": "center", "gap": "15px",
                   "padding": "10px 20px", "background": "rgba(0, 0, 0, 0.65)",
                   "color": "white"},
            children=[
                html.Img(src=app.get_asset_url("logo.png"),
                         style={"height": "70px", "width": "70px"}),
                html.Div([
                    html.H1("The6FlipACoiners", style={"margin": "0", "fontSize": "32px"}),
                    html.Div("Protein to DNA converter", style={"opacity": "0.85"}),
                ]),
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
                        # Example buttons
                        html.Div([
                            html.Span("Examples:", style={"fontWeight": "bold", "marginRight": "10px"}),
                            *[
                                html.Button(
                                    name,
                                    id={"type": "example-button", "index": name},
                                    n_clicks=0,
                                    title=details["info"],
                                    style=button_style,
                                )
                                for name, details in examples.items()
                            ],
                        ], style={"marginBottom": "10px"}),
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
                        html.Button("Convert", id="convert-button", n_clicks=0,
                                    style={**button_style, "fontWeight": "bold"}),
                        html.Div(id="summary", style={"marginTop": "20px", "fontWeight": "bold"}),
                        html.Pre(
                            id="dna-output",
                            style={"whiteSpace": "pre-wrap", "wordBreak": "break-all",
                                   "background": "#f4f4f4", "padding": "10px", "marginTop": "10px"},
                        ),
                        # Copy and download buttons
                        html.Div([
                            html.Button("Copy DNA", id="copy-button", n_clicks=0, style=button_style),
                            html.Button("Download .txt", id="download-txt", n_clicks=0, style=button_style),
                            html.Button("Download FASTA", id="download-fasta", n_clicks=0, style=button_style),
                            html.Span(id="copy-status", style={"marginLeft": "10px", "color": "green"}),
                        ]),
                        dcc.Download(id="download"),
                    ],
                ),
                # Side column: searchable amino acid table
                html.Div(
                    style={**card_style, "flex": "none"},
                    children=[
                        html.H3("Amino acid codes", style={"marginTop": "0"}),
                        dcc.Input(
                            id="aa-search",
                            type="text",
                            placeholder="Search name or code...",
                            debounce=False,
                            style={"width": "100%", "boxSizing": "border-box", "marginBottom": "10px",
                                   "padding": "6px"},
                        ),
                        html.Div(id="aa-table", children=make_amino_acid_table()),
                    ],
                ),
            ],
        ),
    ],
)


@app.callback(
    Output("protein-input", "value"),
    Output("dna-output", "children"),
    Output("summary", "children"),
    Input("convert-button", "n_clicks"),
    Input({"type": "example-button", "index": ALL}, "n_clicks"),
    State("protein-input", "value"),
    State("stop-option", "value"),
)
def convert(n_clicks, example_clicks, protein, stop_option):
    protein_box = no_update

    # If an example button was clicked, load that protein into the text box
    trigger = ctx.triggered_id
    if isinstance(trigger, dict):
        protein = examples[trigger["index"]]["sequence"]
        protein_box = protein

    if not protein or not protein.strip():
        return protein_box, "", "Please enter a protein sequence."

    dna, error = protein_to_dna(protein, add_stop="stop" in (stop_option or []))
    if error:
        return protein_box, "", error

    n_aa = len("".join(protein.split()))
    return protein_box, dna, f"{n_aa} amino acids -> {len(dna)} bases"


@app.callback(
    Output("aa-table", "children"),
    Input("aa-search", "value"),
)
def filter_table(search):
    return make_amino_acid_table(search)


@app.callback(
    Output("download", "data"),
    Input("download-txt", "n_clicks"),
    Input("download-fasta", "n_clicks"),
    State("dna-output", "children"),
    prevent_initial_call=True,
)
def download(txt_clicks, fasta_clicks, dna):
    if not dna:
        raise PreventUpdate

    if ctx.triggered_id == "download-fasta":
        lines = [dna[i:i + 70] for i in range(0, len(dna), 70)]
        fasta = ">The6FlipACoiners_protein_to_DNA\n" + "\n".join(lines) + "\n"
        return dcc.send_string(fasta, "dna_sequence.fasta")

    return dcc.send_string(dna, "dna_sequence.txt")


# Copy to clipboard runs in the browser
app.clientside_callback(
    """
    function(n_clicks, text) {
        if (!n_clicks || !text) {
            return window.dash_clientside.no_update;
        }
        navigator.clipboard.writeText(text);
        return "Copied!";
    }
    """,
    Output("copy-status", "children"),
    Input("copy-button", "n_clicks"),
    State("dna-output", "children"),
    prevent_initial_call=True,
)


if __name__ == "__main__":
    app.run(debug=True)
