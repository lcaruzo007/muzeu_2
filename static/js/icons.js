// Configuração e inicialização dos ícones Feather
document.addEventListener('DOMContentLoaded', function() {
    // Verificar se feather está disponível
    if (typeof feather === 'undefined') {
        console.error('Feather icons não está carregado');
        return;
    }

    // Função para substituir ícones com tratamento de erro robusto
    function replaceIcons(options = {}) {
        try {
            // Encontrar todos os elementos com data-feather
            const featherElements = document.querySelectorAll('[data-feather]');
            
            featherElements.forEach(element => {
                const iconName = element.getAttribute('data-feather');
                if (iconName && feather.icons[iconName]) {
                    try {
                        const svg = feather.icons[iconName].toSvg({
                            'stroke-width': options['stroke-width'] || 2,
                            'width': options.width || 20,
                            'height': options.height || 20,
                            ...options
                        });
                        element.outerHTML = svg;
                    } catch (err) {
                        console.warn(`Erro ao processar ícone ${iconName}:`, err);
                    }
                } else {
                    console.warn(`Ícone não encontrado: ${iconName}`);
                }
            });
        } catch (error) {
            console.error('Erro geral ao substituir ícones:', error);
        }
    }

    // Substituir todos os ícones feather inicialmente
    replaceIcons();
    
    // Aplicar configurações específicas aos ícones da navegação
    setTimeout(() => {
        replaceIcons({
            'stroke-width': 2,
            'width': 18,
            'height': 18
        });
    }, 100);
    
    // Re-inicializar ícones quando houver mudanças dinâmicas
    const observer = new MutationObserver(function(mutations) {
        let hasNewNodes = false;
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length > 0) {
                // Verificar se há novos elementos com data-feather
                for (let node of mutation.addedNodes) {
                    if (node.nodeType === 1) { // Element node
                        if (node.hasAttribute && node.hasAttribute('data-feather') || 
                            node.querySelector && node.querySelector('[data-feather]')) {
                            hasNewNodes = true;
                            break;
                        }
                    }
                }
            }
        });
        
        if (hasNewNodes) {
            setTimeout(() => replaceIcons(), 50);
        }
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});

// Função para atualizar ícones manualmente
function updateIcons() {
    if (typeof feather !== 'undefined') {
        // Usar a função personalizada em vez do feather.replace()
        const featherElements = document.querySelectorAll('[data-feather]');
        
        featherElements.forEach(element => {
            const iconName = element.getAttribute('data-feather');
            if (iconName && feather.icons[iconName]) {
                try {
                    const svg = feather.icons[iconName].toSvg({
                        'stroke-width': 2,
                        'width': 20,
                        'height': 20
                    });
                    element.outerHTML = svg;
                } catch (err) {
                    console.warn(`Erro ao atualizar ícone ${iconName}:`, err);
                }
            }
        });
    }
}

// Exportar função para uso global
window.updateIcons = updateIcons;
