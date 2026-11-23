import subprocess,sys

def run_code(code,test_case):
    if not test_case:
        return 'error'
    for i in test_case:
        try:
            r = subprocess.run(
                [sys.executable,'-c',code],
                input=i.input_data + '\n',
                capture_output=True,text=True,timeout=5,
            )
        except subprocess.TimeoutExpired:
            return 'time_limit'
        if r.returncode != 0 or r.stderr:
            return 'error'
        if r.stdout.strip() != i.expected_output.strip():
            return 'wrong_answer'
    return 'accepted'

