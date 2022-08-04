import configparser,os
import rabbit

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(os.path.basename(__file__).split('.')[0]+".cfg")
    rabbit.process_data_to_spreadsheet(config)
    rabbit.merge_worksheet_data('krastk_data.xlsx')
    rabbit.generate_plots('krastk_data.xlsx')
