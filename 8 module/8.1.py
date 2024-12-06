import cProfile
import pstats

def functions_to_profile():
    print("functions_to_profile")

def load_files():
    print("load_files")

def read_database():
    print("read_database")


TASK_FUNCTIONS_ORDER = ['functions_to_profile', 'load_files', 'read_database']

FUNCTIONS_MAP = {
    'functions_to_profile': functions_to_profile,
    'load_files': load_files,
    'read_database': read_database,
}

def profile_functions(functions_order):
    profiler = cProfile.Profile()
    profiler.enable()

    for function_name in functions_order:
        func = FUNCTIONS_MAP[function_name]
        func()

    profiler.disable()

    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats()

    return stats

def format_profile_stats(stats):
    results = []
    total_time = stats.total_tt
    for func_name in TASK_FUNCTIONS_ORDER:
        for func, (cc, nc, tt, ct, callers) in stats.stats.items():
            if func_name in func[2]:
                time_percentage = (tt / total_time) * 100
                results.append(f"{round(tt):.4f}: {int(round(time_percentage))}%")
                break
    return results

def main():
    stats = profile_functions(TASK_FUNCTIONS_ORDER)
    formatted_stats = format_profile_stats(stats)
    print("\n".join(formatted_stats))

if __name__ == '__main__':
    main()

