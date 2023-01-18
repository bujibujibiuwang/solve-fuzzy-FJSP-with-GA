import argparse


def get_args():
    parser = argparse.ArgumentParser(description="hyper parameters")

    parser.add_argument('--cross_rate', default=0.8, type=int, help='cross_rate')
    parser.add_argument('--mutate_rate', default=0.1, type=int, help='mutate_rate')
    parser.add_argument('--pop_size', default=100, type=int, help='pop_size')
    parser.add_argument('--max_generation', default=1000, type=int, help='max_generation')
    parser.add_argument('--elite_number', default=10, type=int, help='elite_strategy')

    args = parser.parse_args()
    return args