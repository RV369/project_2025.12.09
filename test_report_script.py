import os
import subprocess
import sys
import tempfile

EMPLOYEES1_CONTENT = (
    'name,position,completed_tasks,performance,skills,team,experience_years\n'
    'David Chen,Mobile Developer,36,4.6,\"Swift, Kotlin, React Native, iOS\",'
    'Mobile Team,3\n'
    'Elena Popova,Backend Developer,43,4.8,'
    '\"Java, Spring Boot, MySQL, Redis\",'
    'API Team,4\n'
    'Chris Wilson,DevOps Engineer,39,4.7,\"Docker, Jenkins, GitLab CI, AWS\",'
    'Infrastructure Team,5\n'
    'Olga Kuznetsova,Frontend Developer,42,4.6,\"Vue.js, JavaScript, Webpack, '
    'Sass\",Web Team,3\n'
    'Robert Kim,Data Engineer,34,4.7,\"Python, Apache Spark, Airflow, Kafka\",'
    'Data Team,4\n'
    'Julia Martin,QA Engineer,38,4.5,\"Playwright, Jest, API Testing\",'
    'Testing Team,3\n'
    'Tom Anderson,Backend Developer,49,4.9,\"Go, Microservices, gRPC, '
    'PostgreSQL\",API Team,7\n'
    'Lisa Wang,Mobile Developer,33,4.6,\"Flutter, Dart, Android, Firebase\",'
    'Mobile Team,2\n'
    'Mark Thompson,Data Scientist,31,4.7,\"R, Python, TensorFlow, SQL\",'
    'AI Team,4\n'
)

EMPLOYEES2_CONTENT = (
    'name,position,completed_tasks,performance,skills,team,experience_years\n'
    'Alex Ivanov,Backend Developer,45,4.8,'
    '\"Python, Django, PostgreSQL, Docker\",'
    'API Team,5\n'
    'Maria Petrova,Frontend Developer,38,4.7,'
    '\"React, TypeScript, Redux, CSS\",'
    'Web Team,4\n'
    'John Smith,Data Scientist,29,4.6,\"Python, ML, SQL, Pandas\",'
    'AI Team,3\n'
    'Anna Lee,DevOps Engineer,52,4.9,\"AWS, Kubernetes, Terraform, Ansible\",'
    'Infrastructure Team,6\n'
    'Mike Brown,QA Engineer,41,4.5,\"Selenium, Jest, Cypress, Postman\",'
    'Testing Team,4\n'
    'Sarah Johnson,Fullstack Developer,47,4.7,\"JavaScript, Node.js, React, '
    'MongoDB\",Web Team,5\n'
)


def test_report_script_output():
    with tempfile.TemporaryDirectory() as tmpdir:
        file1 = os.path.join(tmpdir, 'employees1.csv')
        file2 = os.path.join(tmpdir, 'employees2.csv')
        with open(file1, 'w', encoding='utf-8') as f:
            f.write(EMPLOYEES1_CONTENT)
        with open(file2, 'w', encoding='utf-8') as f:
            f.write(EMPLOYEES2_CONTENT)
        # Запускаем скрипт как подпроцесс
        script_path = os.path.join(
            os.path.dirname(__file__),
            'report_script.py',
        )
        result = subprocess.run(
            [
                sys.executable,
                script_path,
                '--files',
                file1,
                file2,
                '--report',
                'performance',
            ],
            capture_output=True,
            text=True,
        )
        # Проверяем, что ошибок не было
        assert result.returncode == 0
        output = result.stdout
        # Проверяем наличие заголовка отчёта
        assert 'Report: performance' in output
        # Проверяем наличие ключевых строк в таблице
        assert 'DevOps Engineer' in output
        assert 'Backend Developer' in output
        assert 'Fullstack Developer' in output
        assert 'Data Scientist' in output
        # Удаляем пробелы и сплитуем по переносу строки
        lines = output.strip().split('\n')
        table_lines = [
            line
            for line in lines
            if '|' in line
            and 'Position' not in line
            and 'Average Performance' not in line
        ]
        # Первая строка данных — самая высокая эффективность
        first_row = table_lines[0]
        assert (
            'DevOps Engineer' in first_row or 'Backend Developer' in first_row
        )
        # Проверим конкретные значения
        assert '4.83' in output
        assert '4.65' in output
        assert '4.5' in output
        # Проверим, что строки отсортированы по убыванию
        perf_values = []
        for line in table_lines:
            parts = line.split('|')
            if len(parts) >= 3:
                try:
                    val = float(parts[2].strip())
                    perf_values.append(val)
                except ValueError:
                    continue

        assert perf_values == sorted(perf_values, reverse=True)
