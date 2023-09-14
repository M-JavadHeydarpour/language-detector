import logging
import os
import zipfile
import tarfile
import rarfile
import subprocess


class Code(object):

    @staticmethod
    def extractCode(file_name, file_path):
        extension = file_name[1].lower()
        file_name = file_name[0].lower()

        source_path = file_path + '/' + file_name + '.' + extension
        destination_path = file_path + '/' + file_name
        try:
            if extension == 'zip':
                with zipfile.ZipFile(source_path, 'r') as zip_ref:
                    zip_ref.extractall(destination_path)
            elif extension == 'tar.gz' or extension == 'tgz':
                with tarfile.open(source_path, 'r:gz') as tar_ref:
                    tar_ref.extractall(destination_path)
            elif extension == 'tar':
                with tarfile.open(source_path, 'r') as tar_ref:
                    tar_ref.extractall(destination_path)
            elif extension == 'rar':
                with rarfile.RarFile(source_path, 'r') as rar_ref:
                    rar_ref.extractall(destination_path)
            else:
                print(extension)
                raise Exception("File format not allowed")

            return destination_path
        except Exception as e:
            raise e

    @staticmethod
    def flattenCode(directory):
        """
        :param directory: code directory
        :return: flatten code text
        """
        all_file_contents = []
        for root, directories, files in os.walk(directory):
            for filename in files:
                file_path = os.path.join(root, filename)

                with open(file_path, 'r', encoding='utf-8') as file:
                    file_contents = file.read()
                    all_file_contents.append(file_contents)

        combined_contents = ' '.join(all_file_contents).replace('\n', '').strip()

        return combined_contents


class Detection(object):

    @staticmethod
    def guesslang(codes, code_path='/tmp/code'):
        with open('/tmp/code', "w") as file:
            file.write(codes)

        os_command = f"guesslang {code_path}"
        output = subprocess.check_output(os_command, shell=True, universal_newlines=True).replace('\n', '').split(': ')[
            1]

        return output


def detection(source_code, source_path):
    """
    :param source_path: source code path
    :param source_code: source code name
    :return: language_name
    """

    source_code = source_code.rsplit('.', 1)
    source_path = source_path.rsplit('.', 1)[0]

    data = Code()
    code_path = data.extractCode(file_name=source_code, file_path=source_path)
    flatten_code_data = data.flattenCode(directory=code_path)

    language_detection = Detection()
    return language_detection.guesslang(codes=flatten_code_data)


if __name__ == "__main__":
    code = Code()
    code_data = code.flattenCode(directory='path/paas/opacloud/opacloud/language-detector')

    languageDetection = Detection()
    languageDetection.guesslang(code_data)
