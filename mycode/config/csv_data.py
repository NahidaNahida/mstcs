HEADER_DICT = {
    "RQ1": ['n', '# test_cases', 'ave_time(entire)', 'ave_time(prepare)'],
    "RQ2": ['test_suite', 'mixed_pre_mode', '# test_cases', 'ave_time'],
    "RQ3": ['n','# test_cases', 'ave_fault'],
    "RQ4": ['test_suite', 'angle_values', '# test_cases', 'ave_fault'],
    "RQ5": ['shots', 'ave_time', 'ave_fault']
}


def required_data(rq_name, recorded_list: list[dict]) -> list[list]:
    def data_profile(rq_name, metadata_dict):
        if rq_name == "RQ1":
            return [
                metadata_dict["num_qubits"],
                metadata_dict["num_test_cases"],
                metadata_dict["ave_exe_time"],
                metadata_dict["ave_pre_time"]
            ]
        elif rq_name == "RQ2":
            return [
                metadata_dict["input_name"],
                metadata_dict["controlling_unit"],
                metadata_dict["num_test_cases"],
                metadata_dict["ave_exe_time"]
            ]
        elif rq_name == "RQ3":
            return [
                metadata_dict["num_qubits"],
                metadata_dict["num_test_cases"],
                metadata_dict["ave_faults"]
            ]
        elif rq_name == "RQ4":
            return [
                metadata_dict["input_name"],
                metadata_dict["angle_values"],
                metadata_dict["num_test_cases"],
                metadata_dict["ave_faults"]
            ]
        elif rq_name == "RQ5":
            return [
                metadata_dict["num_shots"],
                metadata_dict["ave_exe_time"],
                metadata_dict["ave_faults"]
            ]
        else:
            raise ValueError(f"Unknown RQ name: {rq_name}")

    recorded_result = [
        data_profile(rq_name, metadata_dict)
        for metadata_dict in recorded_list
    ]
    return recorded_result
