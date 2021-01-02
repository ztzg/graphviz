from subprocess import Popen, PIPE
import os.path, sys
from pathlib import Path

# Import helper function to compare graphs from tests/regressions_tests
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from regression_test_helpers import compare_graphs

shapes = [
    'box',
    'polygon',
    'ellipse',
    'oval',
    'circle',
    'point',
    'egg',
    'triangle',
    'none',
    'plaintext',
    'plain',
    'diamond',
    'trapezium',
    'parallelogram',
    'house',
    'pentagon',
    'hexagon',
    'septagon',
    'octagon',
    'note',
    'tab',
    'folder',
    'box3d',
    'component',
    'cylinder',
    'rect',
    'rectangle',
    'square',
    'star',
    'doublecircle',
    'doubleoctagon',
    'tripleoctagon',
    'invtriangle',
    'invtrapezium',
    'invhouse',
    'underline',
    'Mdiamond',
    'Msquare',
    'Mcircle',
    # biological circuit shapes
    # gene expression symbols
    'promoter',
    'cds',
    'terminator',
    'utr',
    'insulator',
    'ribosite',
    'rnastab',
    'proteasesite',
    'proteinstab',
    # dna construction symbols
    'primersite',
    'restrictionsite',
    'fivepoverhang',
    'threepoverhang',
    'noverhang',
    'assembly',
    'signature',
    'rpromoter',
    'larrow',
    'rarrow',
    'lpromoter'
]

output_types = [
    'gv',
    'svg',
    'xdot'
]

def generate_shape_graph(shape, output_type):
    if not Path('output').exists():
        Path('output').mkdir(parents=True)

    output_file = Path('output') / (shape + '.' + output_type)
    process = Popen(['dot', '-T' + output_type, '-o', output_file], stdin=PIPE)

    input_graph = 'graph G { a [label="" shape=' + shape + '] }'
    process.communicate(input = input_graph.encode('utf_8'))

    if process.wait() != 0:
        print('An error occurred while generating: ' + str(output_file))
        exit(1)

    if output_type == 'svg':
        # Remove the number in 'Generated by graphviz version <number>'
        # to able to compare the output to the reference. This version
        # number is different for every Graphviz compilation.
        file = open(output_file, 'r')
        lines = file.readlines()
        file.close()

        file = open(output_file, 'w')
        for line in lines:
            if '<!-- Generated by graphviz version ' in line:
                file.write('<!-- Generated by graphviz version\n')
            else:
                file.write(line)

failures = 0
for shape in shapes:
    for output_type in output_types:
        generate_shape_graph(shape, output_type)
        if not compare_graphs(shape, output_type):
            failures += 1

print('')
print('Results for "shapes" regression test:')
print('    Number of tests: ' + str(len(shapes) * len(output_types)))
print('    Number of failures: ' + str(failures))

if not failures == 0:
    exit(1) 
