/***************************************************** Variables  ****************************************************/
const vacancy_vid = JSON.parse(document.getElementById('json-vacancy_vid').textContent)
const numDocuments = document.getElementById('numDocuments');
const btnStart = document.getElementById('btnStart');
const container = document.getElementById('default-chat-container');
const rows = document.querySelectorAll("table tbody tr");

let chatSocket = null;

const removeForm = ()=>{
    document.getElementById('formContainer').remove();
}

const alterTable = (data)=>{
    rows.forEach(row => {
        const link = row.querySelector("a.cvLink");
        if (link) {
            const href = link.getAttribute('href');
            const match = data.find(item => href.includes(item.filename));
            if (match) {
                const compatibilityCell = row.querySelector('.compatibility');
                const summaryCell = row.querySelector('.summary');

                compatibilityCell.textContent = match.compatibility;
                summaryCell.textContent = match.summary;

                compatibilityCell.classList.add('alert-success');
                summaryCell.classList.add('alert-success');
            } else {
                row.remove();
            }
        }
    });
}

const setBtnProcessing = ()=>{
    let child = `
        <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
        Processando...
    `;
    btnStart.innerHTML=``;
    btnStart.setAttribute('disabled', true);
    btnStart.insertAdjacentHTML('beforeend', child);
};

const setBtnAnalyzing = ()=>{
    let child = `
    <span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>
    Analisando Documentos...`;
    btnStart.innerHTML=``;
    btnStart.setAttribute('disabled', true);
    btnStart.insertAdjacentHTML('beforeend', child);
}

btnStart.addEventListener('click', () => {
    if(!numDocuments.value)
    {
        alert("Preencha o número de documentos que devem ser retornados!");
        return;
    }

    setBtnProcessing();
        
    chatSocket = new WebSocket(`ws://${window.location.host}/ws/analisar-candidaturas/${vacancy_vid}/${numDocuments.value}/`);
    chatSocket.onopen = function(e) {
        console.log('Conexão estabelecida.');
        // window.alert('Conexão estabelecida.');
        setBtnAnalyzing();
        chatSocket.send(JSON.stringify({"message": "data"}))
    };
        

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data)
        console.log("Data Received:", data);
        try {
            if(data.type==='response')
            {
                removeForm();
                alterTable(data.data);
                Swal.fire({
                    title: "Análise de Cvs!",
                    text: "Documentos analisados com sucesso!",
                    icon: "success"
                });
            }
        } 
        catch (error) 
        {
            // console.error(error);
            Swal.fire({
                title: "Analise de Cvs!",
                text: "Error ao ler os dados dos Cvs!",
                icon: "error"
              });
        }
    }
        
    chatSocket.onclose = function() {
        console.log('Conexão fechada.');
        // window.alert("Conexão fechada");
    };
        
});


window.addEventListener('load', ()=>{
   
})