import argparse
import os

from mitreattack.navlayers.generators.overview_generator import OverviewLayerGenerator
from mitreattack.navlayers.generators.usage_generator import UsageLayerGenerator
from mitreattack.navlayers.generators.sum_generator import BatchGenerator


def main():
    parser = argparse.ArgumentParser(description='Generate an ATT&CK Navigator layer')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--overview-type', choices=['group', 'software', 'mitigation'],
                       help='Output a layer file where the target type is summarized across the entire dataset.')
    group.add_argument('--mapped-to', help='Output layer file with techniques mapped to the given group, software, or '
                                           'mitigation. Argument can be name, associated group/software, or ATT&CK ID.')
    group.add_argument('--batch-type', choices=['group', 'software', 'mitigation'],
                       help='Output a collection of layer files to the specified folder, each one representing a '
                            'different instance of the target type.')
    parser.add_argument('-o', '--output', help='Path to the output layer file/directory', default='generated_layer')
    parser.add_argument('--domain', help='Which domain to build off of', choices=['enterprise', 'mobile', 'ics'],
                        default='enterprise')
    parser.add_argument('--source', choices=['taxii', 'local'], default='taxii',
                        help='What source to utilize when building the layer files')
    parser.add_argument('--local', help='Path to the local resource if --source=local', default=None)
    args = parser.parse_args()

    if args.overview_type:
        og = OverviewLayerGenerator(source=args.source, domain=args.domain, local=args.local)
        generated = og.generate_layer(obj_type=args.overview_type)
        print('Generating Layer File')
        out_path = args.output
        if out_path == 'generated_layer':
            out_path += '.json'
        generated.to_file(out_path)
        print(f'Layer file generated as {out_path}.')
    elif args.mapped_to:
        ug = UsageLayerGenerator(source=args.source, domain=args.domain, local=args.local)
        generated = ug.generate_layer(match=args.mapped_to)
        print('Generating Layer File')
        out_path = args.output
        if out_path == 'generated_layer':
            out_path += '.json'
        generated.to_file(out_path)
        print(f'Layer file generated as {out_path}.')
    elif args.batch_type:
        bg = BatchGenerator(source=args.source, domain=args.domain, local=args.local)
        generated = bg.generate_layers(layers_type=args.batch_type)
        out_path = args.output
        if out_path == 'generated_layer':
            out_path += 's'
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        for sid in generated:
            generated[sid].to_file(f"{out_path}/{sid}.json")
        print(f"Files saved to {out_path}/")


if __name__ == '__main__':
    main()
