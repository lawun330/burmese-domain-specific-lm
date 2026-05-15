import sys, math

def evaluate(model, test_path, print_stats=False):

    sum_log10 = 0.0
    n_words = 0
    n_chars = 0

    with open(test_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            for prob, length, oov in model.full_scores(line):
                sum_log10 += prob
                n_words += 1  # counts </s> token too
            n_chars += len(line)

    # sum_log10 is negative → negate once for all positive quantities
    sum_nats   = -sum_log10 * math.log(10)
    total_bits = -sum_log10 * math.log2(10)

    perplexity = math.exp(sum_nats / n_words) if n_words else float("inf")
    entropy = sum_nats / n_words if n_words else float("inf")
    bits_per_character = total_bits / n_chars if n_chars else float("inf")

    if print_stats:
        print(f"Perplexity (PPL): {perplexity:.2f}")
        print(f"Entropy: {entropy:.4f} nats")
        print(f"Bits per character (BPC): {bits_per_character:.4f}")

    return perplexity, entropy, bits_per_character

if __name__ == "__main__":
    evaluate(sys.argv[1], sys.argv[2], sys.argv[3])