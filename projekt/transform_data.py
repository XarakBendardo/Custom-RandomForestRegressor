from src.DataProcessor import DataProcessor


def main():
    DataProcessor.get_data_from_file()
    DataProcessor.transform_data()
    DataProcessor.save_transformed_data()


if __name__ == "__main__":
    main()
