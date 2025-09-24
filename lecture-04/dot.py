from graphviz import Digraph
dot_compact = Digraph(comment="Evolutionary Fuzzing Framework", format="png")
dot_compact.attr(rankdir='TB', fontsize='12', style='rounded')  # Top to Bottom layout

# Nodes
dot_compact.node("SeedPool", "Seed Corpus / Input Queue", shape="box", style="rounded,filled", fillcolor="#4F81BD", fontcolor="white")
dot_compact.node("Mutation", "Mutation Engine\n(Bit flips, Arithmetic, Splicing, etc.)", shape="box", style="rounded,filled", fillcolor="#C0504D", fontcolor="white")
dot_compact.node("Execution", "Program Execution\n(Target Program)", shape="box", style="rounded,filled", fillcolor="#9BBB59", fontcolor="white")
dot_compact.node("Coverage", "Coverage Feedback\n(Edge/Block Coverage)", shape="box", style="rounded,filled", fillcolor="#8064A2", fontcolor="white")
dot_compact.node("Selection", "Selection & Prioritization\n(Based on Coverage Gains)", shape="box", style="rounded,filled", fillcolor="#F79646", fontcolor="white")
dot_compact.node("CrashDB", "Crash / Hang Detection\n& Minimization", shape="box", style="rounded,filled", fillcolor="#4BACC6", fontcolor="white")

# Edges
dot_compact.edge("SeedPool", "Mutation", label="Select Seed")
dot_compact.edge("Mutation", "Execution", label="Mutated Input")
dot_compact.edge("Execution", "Coverage", label="Trace Coverage Data")
dot_compact.edge("Coverage", "Selection", label="Coverage Metrics")
dot_compact.edge("Selection", "SeedPool", label="Add Interesting Inputs")
dot_compact.edge("Execution", "CrashDB", label="Detect Crashes/Hangs")

# Render to PNG
png_compact_path = "./evolutionary_fuzzing_framework_compact.png"
dot_compact.render(png_compact_path, cleanup=True)
