# run_evaluation.py
import os
import json
from evaluation.evaluation_guard import evaluation_result

def main():
    """
    Run evaluation guards and display results.
    """
    # Ensure the results folder exists
    results_dir = os.path.join("data", "evaluation_results")
    os.makedirs(results_dir, exist_ok=True)

    # Run evaluation (with a default dummy plan)
    result = evaluation_result()

    # Save results to JSON
    results_path = os.path.join(results_dir, "evaluation_result.json")
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    # Print results
    print("Evaluation Result:")
    print(result)
    print(f"\n✅ Results saved to {results_path}")

if __name__ == "__main__":
    main()
