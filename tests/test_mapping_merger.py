from app.git.mapping_merger import MappingMerger


BASE_COMMIT = (
    "76dc6ae7cc1376ea67f8ad3f06125489e2e4888a"
)

TARGET_COMMIT = (
    "0a15a7fd7b030b9a06d511cd9d6add62259e8932"
)


def test_mapping_merger():

    merger = MappingMerger()

    result = merger.merge(
        base_mapping_path=(
            f"outputs/commits/"
            f"{BASE_COMMIT}/"
            f"validated_mapping.json"
        ),

        target_mapping_path=(
            f"outputs/commits/"
            f"{TARGET_COMMIT}/"
            f"reevaluation/"
            f"validated_mapping.json"
        ),

        selection_path=(
            "outputs/evaluation_selection.json"
        ),
    )

    output_path = (
        f"outputs/commits/"
        f"{TARGET_COMMIT}/"
        f"validated_mapping.json"
    )

    merger.save_result(
        result,
        output_path,
    )

    print()
    print("=" * 70)
    print("TARGET MAPPING MERGE")
    print("=" * 70)

    print()

    for mapping in result:

        print(
            f"{mapping.get('ac_id')}: "
            f"{mapping.get('mapping_source')}"
        )

    print()
    print("Total Mappings:", len(result))

    print()
    print("=" * 70)
    print(
        "Output:",
        output_path,
    )
    print("=" * 70)


if __name__ == "__main__":
    test_mapping_merger()