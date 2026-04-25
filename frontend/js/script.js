async function more_than_3_twos() {
    const response = await fetch('http://185.182.65.215:8000/students/more-than-3-twos');
    const data = await response.json();
    let displayText = "Студентов не найдено";
    if (data.length > 0) {
        displayText = data.map(student => `${student.full_name} - ${student.count_twos}`).join('\n');
    }
    document.getElementById('output').innerText = displayText;
}

async function less_than_5_twos() {
    const response = await fetch('http://185.182.65.215:8000/students/less-than-5-twos');
    const data = await response.json();
    let displayText = "Студентов не найдено";
    if (data.length > 0) {
        displayText = data.map(student => `${student.full_name} - ${student.count_twos}`).join('\n');
    }
    document.getElementById('output').innerText = displayText;
}

async function handler_file_csv(event) {
    event.preventDefault();
    const formData = new FormData();
    const fileInput = document.getElementById('fileInput');
    formData.append('data', fileInput.files[0]);
    const response = await fetch('http://185.182.65.215:8000/upload-grades', { method: 'POST', body: formData });
    const result = await response.json();
    document.getElementById('output_load').innerText = `Успех! Загружено записей: ${result.records_loaded}`;
}

const myForm = document.getElementById('uploadForm');
myForm.addEventListener('submit', handler_file_csv);