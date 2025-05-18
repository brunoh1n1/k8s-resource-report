🔍 Kubernetes Resource Usage Inspector

Este script inspeciona o cluster Kubernetes e gera um relatório detalhado sobre a utilização de recursos por namespace, sugerindo possíveis melhorias com base no uso real versus os recursos solicitados (requests) e limites (limits).
📦 Funcionalidades

    Coleta uso de CPU e memória por namespace.

    Compara requests e limits configurados com o uso real.

    Gera recomendações de ajuste de recursos.

    Ajuda a identificar:

        Overprovisioning (recursos pedidos muito acima do uso).

        Underprovisioning (uso maior que os limites).

        Namespaces ociosos.

🚀 Requisitos

    Python 3.6+

    Acesso a um cluster Kubernetes configurado no kubectl

    Permissões para listar pods e métricas

📦 Instale as dependências:

pip install kubernetes tabulate

▶️ Como usar

python3 k8s_resource_report.py

    O script conecta no cluster atual configurado com kubectl config current-context e imprime um relatório no terminal.

✅ Exemplo de saída:

Namespace    CPU Usage    CPU Requests    Mem Usage    Mem Requests    Recommendations
---------    -----------  -------------   ----------   -------------   --------------------------
default      120m         1000m           512Mi        2Gi             Ajustar CPU requests
kube-system  80m          150m            256Mi        512Mi           OK
dev          0m           500m            10Mi         1Gi             Recursos ociosos

💡 Sugestões automáticas

O script analisa e sugere melhorias, como:

    Reduzir requests se o uso estiver consistentemente baixo.

    Aumentar limits se estiverem sendo atingidos.

    Eliminar ou escalar down namespaces sem atividade.

📁 Arquivo de saída

Você pode editar o script para salvar a saída como .csv, .md ou .html para integração com dashboards ou documentação.
🛠️ To-do (contribuições bem-vindas!)

    Exportação para CSV/Markdown

    Geração de gráfico de uso

    Envio automático para Slack ou email

    Integração com Prometheus