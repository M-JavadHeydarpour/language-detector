import os
import zipfile
import tarfile
import rarfile
import subprocess


class Code(object):

    @staticmethod
    def extractCode(file_name, file_path):
        extension = file_name.rsplit('.', 1)[1].lower()
        destination_path = file_path + file_name.rsplit('.', 1)[0].lower()
        try:
            if extension == '.zip':
                with zipfile.ZipFile(file_path + file_name, 'r') as zip_ref:
                    zip_ref.extractall(destination_path)
            elif extension == '.tar.gz' or extension == '.tgz':
                with tarfile.open(file_path + file_name, 'r:gz') as tar_ref:
                    tar_ref.extractall(destination_path)
            elif extension == '.tar':
                with tarfile.open(file_path + file_name, 'r') as tar_ref:
                    tar_ref.extractall(destination_path)
            elif extension == '.rar':
                with rarfile.RarFile(file_path + file_name, 'r') as rar_ref:
                    rar_ref.extractall(destination_path)
            else:
                raise Exception("File format not allowed")

            return True
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
    data = Code()
    data.extractCode(file_name=source_code, file_path=source_path)
    flatten_code_data = data.flattenCode(directory=source_path + source_code)

    language_detection = Detection()
    return language_detection.guesslang(flatten_code_data)


if __name__ == "__main__":
    code = Code()
    code_data = code.flattenCode(directory='path/paas/opacloud/opacloud/language-detector')

    languageDetection = Detection()
    languageDetection.guesslang(code_data)
