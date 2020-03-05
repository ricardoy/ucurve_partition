from lattice import Partition
from robdd import Robdd


def get_minimal_element(robdd:Robdd, mapping_partition_to_boolean, mapping_boolean_to_partition, expected_value=1):
    bool_representation = robdd.get_random_solution(expected_value)
    if bool_representation is None:
        return None

    partition = Partition(mask=mapping_boolean_to_partition[tuple(bool_representation)].mask)

    while True:
        can_continue = False
        for partition_child in partition.subset_generator():
            boolean_representation = mapping_partition_to_boolean[partition_child.mask]
            if robdd.evaluate(boolean_representation) == expected_value:
                can_continue = True
                partition = partition_child

        if not can_continue:
            break

    return mapping_partition_to_boolean[partition.mask]