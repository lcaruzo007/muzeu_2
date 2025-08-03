// Gerenciador de Modals
class ModalManager {
    constructor() {
        this.activeModal = null;
        this.init();
    }

    init() {
        // Event listeners para botões que abrem modals
        document.addEventListener('click', (e) => {
            if (e.target.hasAttribute('data-modal')) {
                const modalId = e.target.getAttribute('data-modal');
                this.openModal(modalId);
            }
            
            // Fechar modal ao clicar no overlay
            if (e.target.classList.contains('modal-overlay')) {
                this.closeModal();
            }
            
            // Fechar modal ao clicar no botão de fechar
            if (e.target.classList.contains('modal-close')) {
                this.closeModal();
            }
        });

        // Fechar modal com ESC
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.activeModal) {
                this.closeModal();
            }
        });
    }

    openModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            this.activeModal = modal;
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        }
    }

    closeModal(element) {
        // Se um elemento for passado, fecha o modal-overlay mais próximo
        if (element) {
            let overlay = element.closest('.modal-overlay');
            if (overlay) {
                overlay.classList.remove('active');
                document.body.style.overflow = '';
                if (this.activeModal === overlay) this.activeModal = null;
                return;
            }
        }
        // Caso contrário, fecha o activeModal
        if (this.activeModal) {
            this.activeModal.classList.remove('active');
            document.body.style.overflow = '';
            this.activeModal = null;
        }
    }
}

// Gerenciador de Sidebar
class SidebarManager {
    constructor() {
        this.sidebar = document.querySelector('.sidebar');
        this.mainContent = document.querySelector('.main-content');
        this.toggleBtn = document.querySelector('.sidebar-toggle');
        this.init();
    }

    init() {
        if (this.toggleBtn) {
            this.toggleBtn.addEventListener('click', () => {
                this.toggle();
            });
        }

        // Fechar sidebar no mobile ao clicar fora
        document.addEventListener('click', (e) => {
            if (window.innerWidth <= 768) {
                if (!this.sidebar.contains(e.target) && !e.target.classList.contains('sidebar-toggle')) {
                    this.close();
                }
            }
        });
    }

    toggle() {
        if (window.innerWidth <= 768) {
            this.sidebar.classList.toggle('mobile-open');
        } else {
            this.sidebar.classList.toggle('collapsed');
            this.mainContent.classList.toggle('expanded');
        }
    }

    close() {
        this.sidebar.classList.remove('mobile-open');
    }
}

// Gerenciador de Formulários
class FormManager {
    constructor() {
        this.init();
    }

    init() {
        // Event listeners para modais
        document.addEventListener('click', (e) => {
            if (e.target.hasAttribute('data-modal')) {
                const modalId = e.target.getAttribute('data-modal');
                this.openModal(modalId);
            }
            // Fechar modal ao clicar no overlay
            if (e.target.classList.contains('modal-overlay')) {
                this.closeModal(e.target);
            }
            // Fechar modal ao clicar no botão de fechar
            if (e.target.classList.contains('modal-close')) {
                this.closeModal(e.target);
            }
        });

        // Validação em tempo real dos formulários
        document.addEventListener('input', (e) => {
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
                this.validateField(e.target);
            }
        });
    }

    validateField(field) {
        const value = field.value.trim();
        const type = field.type;
        let isValid = true;
        let message = '';

        // Remover classes de erro anteriores
        field.classList.remove('error', 'success');
        this.removeFieldMessage(field);

        // Validações básicas
        if (field.hasAttribute('required') && !value) {
            isValid = false;
            message = 'Este campo é obrigatório';
        } else if (type === 'email' && value && !this.isValidEmail(value)) {
            isValid = false;
            message = 'Email inválido';
        } else if (field.name === 'cpf' && value && !this.isValidCPF(value)) {
            isValid = false;
            message = 'CPF inválido';
        }

        // Aplicar estilos e mensagens
        if (!isValid) {
            field.classList.add('error');
            this.showFieldMessage(field, message, 'error');
        } else if (value) {
            field.classList.add('success');
        }

        return isValid;
    }

    isValidEmail(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    }

    isValidCPF(cpf) {
        cpf = cpf.replace(/[^\d]/g, '');
        
        if (cpf.length !== 11 || /^(\d)\1{10}$/.test(cpf)) {
            return false;
        }

        let sum = 0;
        for (let i = 0; i < 9; i++) {
            sum += parseInt(cpf.charAt(i)) * (10 - i);
        }
        
        let remainder = 11 - (sum % 11);
        let digit1 = remainder < 2 ? 0 : remainder;
        
        if (parseInt(cpf.charAt(9)) !== digit1) {
            return false;
        }

        sum = 0;
        for (let i = 0; i < 10; i++) {
            sum += parseInt(cpf.charAt(i)) * (11 - i);
        }
        
        remainder = 11 - (sum % 11);
        let digit2 = remainder < 2 ? 0 : remainder;
        
        return parseInt(cpf.charAt(10)) === digit2;
    }

    showFieldMessage(field, message, type) {
        const messageEl = document.createElement('div');
        messageEl.className = `field-message ${type}`;
        messageEl.textContent = message;
        field.parentNode.appendChild(messageEl);
    }

    removeFieldMessage(field) {
        const message = field.parentNode.querySelector('.field-message');
        if (message) {
            message.remove();
        }
    }

    async handleFormSubmit(form) {
        const submitBtn = form.querySelector('[type="submit"]');
        const originalText = submitBtn.textContent;
        
        // Mostrar loading
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="loading"></span> Enviando...';

        try {
            const formData = new FormData(form);
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });

            const result = await response.json();

            if (response.ok && result.success) {
                this.showNotification('Operação realizada com sucesso!', 'success');
                if (result.redirect) {
                    window.location.href = result.redirect;
                } else {
                    form.reset();
                    modalManager.closeModal();
                }
            } else {
                this.showNotification(result.message || 'Erro ao processar solicitação', 'error');
            }
        } catch (error) {
            this.showNotification('Erro de conexão', 'error');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
        }
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <span>${message}</span>
            <button class="notification-close">&times;</button>
        `;

        document.body.appendChild(notification);

        // Auto remove após 5 segundos
        setTimeout(() => {
            notification.remove();
        }, 5000);

        // Remover ao clicar no X
        notification.querySelector('.notification-close').addEventListener('click', () => {
            notification.remove();
        });
    }
}

// Gerenciador de Modelos 3D
class Model3DViewer {
    constructor(container, modelUrl) {
        this.container = container;
        this.modelUrl = modelUrl;
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        this.model = null;
        this.init();
    }

    async init() {
        if (!window.THREE) {
            await this.loadThreeJS();
        }

        this.setupScene();
        this.setupCamera();
        this.setupRenderer();
        this.setupControls();
        this.setupLights();
        
        if (this.modelUrl) {
            await this.loadModel();
        }

        this.animate();
        this.setupControls();
    }

    async loadThreeJS() {
        return new Promise((resolve) => {
            const script = document.createElement('script');
            script.src = 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js';
            script.onload = () => {
                // Carregar GLTFLoader
                const loaderScript = document.createElement('script');
                loaderScript.src = 'https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js';
                loaderScript.onload = resolve;
                document.head.appendChild(loaderScript);
            };
            document.head.appendChild(script);
        });
    }

    setupScene() {
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0xf0f0f0);
    }

    setupCamera() {
        const aspect = this.container.clientWidth / this.container.clientHeight;
        this.camera = new THREE.PerspectiveCamera(75, aspect, 0.1, 1000);
        this.camera.position.set(0, 0, 5);
    }

    setupRenderer() {
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        this.container.appendChild(this.renderer.domElement);
    }

    setupControls() {
        // Usar OrbitControls se disponível
        if (window.THREE.OrbitControls) {
            this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
            this.controls.enableDamping = true;
            this.controls.dampingFactor = 0.05;
        }
    }

    setupLights() {
        // Luz ambiente
        const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
        this.scene.add(ambientLight);

        // Luz direcional
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(10, 10, 5);
        directionalLight.castShadow = true;
        this.scene.add(directionalLight);
    }

    async loadModel() {
        try {
            const loader = new THREE.GLTFLoader();
            const gltf = await new Promise((resolve, reject) => {
                loader.load(this.modelUrl, resolve, undefined, reject);
            });

            this.model = gltf.scene;
            this.scene.add(this.model);

            // Centralizar modelo
            const box = new THREE.Box3().setFromObject(this.model);
            const center = box.getCenter(new THREE.Vector3());
            this.model.position.sub(center);

            // Ajustar câmera
            const size = box.getSize(new THREE.Vector3());
            const maxDim = Math.max(size.x, size.y, size.z);
            this.camera.position.z = maxDim * 2;

        } catch (error) {
            console.error('Erro ao carregar modelo 3D:', error);
            this.showError('Erro ao carregar modelo 3D');
        }
    }

    animate() {
        requestAnimationFrame(() => this.animate());

        if (this.controls) {
            this.controls.update();
        }

        this.renderer.render(this.scene, this.camera);
    }

    resetView() {
        if (this.model) {
            this.camera.position.set(0, 0, 5);
            if (this.controls) {
                this.controls.reset();
            }
        }
    }

    toggleWireframe() {
        if (this.model) {
            this.model.traverse((child) => {
                if (child.isMesh) {
                    child.material.wireframe = !child.material.wireframe;
                }
            });
        }
    }

    showError(message) {
        this.container.innerHTML = `
            <div class="model-3d-error">
                <i class="icon-alert-circle"></i>
                <p>${message}</p>
            </div>
        `;
    }

    dispose() {
        if (this.renderer) {
            this.renderer.dispose();
        }
        if (this.controls) {
            this.controls.dispose();
        }
    }
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    // Inicializar gerenciadores
    window.modalManager = new ModalManager();
    window.sidebarManager = new SidebarManager();
    window.formManager = new FormManager();

    // Inicializar visualizadores 3D
    document.querySelectorAll('.model-3d-container').forEach(container => {
        const modelUrl = container.getAttribute('data-model-url');
        if (modelUrl) {
            new Model3DViewer(container.querySelector('.model-3d-viewer'), modelUrl);
        }
    });

    // Máscara para CPF
    document.querySelectorAll('input[name="cpf"]').forEach(input => {
        input.addEventListener('input', (e) => {
            let value = e.target.value.replace(/\D/g, '');
            value = value.replace(/(\d{3})(\d)/, '$1.$2');
            value = value.replace(/(\d{3})(\d)/, '$1.$2');
            value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
            e.target.value = value;
        });
    });

    // Smooth scroll para links internos
    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = document.querySelector(link.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
});
