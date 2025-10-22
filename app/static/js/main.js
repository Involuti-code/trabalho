// Sistema Administrativo-Financeiro - JavaScript Principal

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Inicializar popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts após 5 segundos
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Confirmar exclusão
    document.querySelectorAll('.btn-delete').forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Tem certeza que deseja excluir este item?')) {
                e.preventDefault();
            }
        });
    });

    // Formatação de moeda
    document.querySelectorAll('.currency-input').forEach(function(input) {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            value = (value / 100).toLocaleString('pt-BR', {
                style: 'currency',
                currency: 'BRL'
            });
            e.target.value = value;
        });
    });

    // Formatação de CPF/CNPJ
    document.querySelectorAll('.cpf-input').forEach(function(input) {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length <= 11) {
                value = value.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
            } else {
                value = value.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5');
            }
            e.target.value = value;
        });
    });

    // Formatação de telefone
    document.querySelectorAll('.phone-input').forEach(function(input) {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length <= 10) {
                value = value.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
            } else {
                value = value.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
            }
            e.target.value = value;
        });
    });

    // Upload de arquivo com drag and drop
    const fileUploadAreas = document.querySelectorAll('.file-upload-area');
    fileUploadAreas.forEach(function(area) {
        const input = area.querySelector('input[type="file"]');
        
        area.addEventListener('click', function() {
            input.click();
        });

        area.addEventListener('dragover', function(e) {
            e.preventDefault();
            area.classList.add('dragover');
        });

        area.addEventListener('dragleave', function(e) {
            e.preventDefault();
            area.classList.remove('dragover');
        });

        area.addEventListener('drop', function(e) {
            e.preventDefault();
            area.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                input.files = files;
                updateFileDisplay(area, files[0]);
            }
        });

        input.addEventListener('change', function(e) {
            if (e.target.files.length > 0) {
                updateFileDisplay(area, e.target.files[0]);
            }
        });
    });

    // Atualizar display do arquivo
    function updateFileDisplay(area, file) {
        const display = area.querySelector('.file-display');
        if (display) {
            display.innerHTML = `
                <i class="bi bi-file-earmark-pdf text-danger"></i>
                <div class="mt-2">
                    <strong>${file.name}</strong><br>
                    <small class="text-muted">${formatFileSize(file.size)}</small>
                </div>
            `;
        }
    }

    // Formatar tamanho do arquivo
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    // Busca em tempo real
    document.querySelectorAll('.search-input').forEach(function(input) {
        let timeout;
        input.addEventListener('input', function(e) {
            clearTimeout(timeout);
            timeout = setTimeout(function() {
                performSearch(e.target.value);
            }, 300);
        });
    });

    // Função de busca
    function performSearch(query) {
        const table = document.querySelector('.searchable-table');
        if (!table) return;

        const rows = table.querySelectorAll('tbody tr');
        rows.forEach(function(row) {
            const text = row.textContent.toLowerCase();
            if (text.includes(query.toLowerCase())) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }

    // Filtros de data
    document.querySelectorAll('.date-filter').forEach(function(input) {
        input.addEventListener('change', function() {
            applyDateFilter();
        });
    });

    function applyDateFilter() {
        const startDate = document.querySelector('#start-date')?.value;
        const endDate = document.querySelector('#end-date')?.value;
        
        if (!startDate || !endDate) return;

        const table = document.querySelector('.date-filterable-table');
        if (!table) return;

        const rows = table.querySelectorAll('tbody tr');
        rows.forEach(function(row) {
            const dateCell = row.querySelector('.date-cell');
            if (!dateCell) return;

            const rowDate = new Date(dateCell.textContent);
            const start = new Date(startDate);
            const end = new Date(endDate);

            if (rowDate >= start && rowDate <= end) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }

    // Exportar para CSV
    document.querySelectorAll('.btn-export-csv').forEach(function(button) {
        button.addEventListener('click', function() {
            const table = document.querySelector('.exportable-table');
            if (!table) return;

            let csv = [];
            const rows = table.querySelectorAll('tr');
            
            rows.forEach(function(row) {
                const cells = row.querySelectorAll('td, th');
                const rowData = Array.from(cells).map(cell => {
                    return '"' + cell.textContent.replace(/"/g, '""') + '"';
                });
                csv.push(rowData.join(','));
            });

            const csvContent = csv.join('\n');
            const blob = new Blob([csvContent], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'export.csv';
            a.click();
            window.URL.revokeObjectURL(url);
        });
    });

    // Modal de confirmação
    window.showConfirmModal = function(title, message, callback) {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">${title}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <p>${message}</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-primary" id="confirm-btn">Confirmar</button>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();

        document.getElementById('confirm-btn').addEventListener('click', function() {
            callback();
            bsModal.hide();
        });

        modal.addEventListener('hidden.bs.modal', function() {
            document.body.removeChild(modal);
        });
    };

    // Notificações toast
    window.showToast = function(message, type = 'info') {
        const toastContainer = document.querySelector('.toast-container') || createToastContainer();
        
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type} border-0`;
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;

        toastContainer.appendChild(toast);
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();

        toast.addEventListener('hidden.bs.toast', function() {
            toastContainer.removeChild(toast);
        });
    };

    function createToastContainer() {
        const container = document.createElement('div');
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '1055';
        document.body.appendChild(container);
        return container;
    }

    // Loading overlay
    window.showLoading = function() {
        const overlay = document.createElement('div');
        overlay.id = 'loading-overlay';
        overlay.className = 'position-fixed top-0 start-0 w-100 h-100 d-flex justify-content-center align-items-center';
        overlay.style.backgroundColor = 'rgba(0,0,0,0.5)';
        overlay.style.zIndex = '9999';
        overlay.innerHTML = `
            <div class="spinner-border text-light" role="status">
                <span class="visually-hidden">Carregando...</span>
            </div>
        `;
        document.body.appendChild(overlay);
    };

    window.hideLoading = function() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            document.body.removeChild(overlay);
        }
    };

    // Validação de formulários
    document.querySelectorAll('form').forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Auto-save em formulários
    document.querySelectorAll('.auto-save').forEach(function(form) {
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(function(input) {
            input.addEventListener('change', function() {
                saveFormData(form);
            });
        });
    });

    function saveFormData(form) {
        const formData = new FormData(form);
        const data = {};
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        localStorage.setItem('form_' + form.id, JSON.stringify(data));
    }

    // Restaurar dados do formulário
    document.querySelectorAll('.auto-save').forEach(function(form) {
        const savedData = localStorage.getItem('form_' + form.id);
        if (savedData) {
            const data = JSON.parse(savedData);
            Object.keys(data).forEach(function(key) {
                const input = form.querySelector(`[name="${key}"]`);
                if (input) {
                    input.value = data[key];
                }
            });
        }
    });

    // Limpar dados salvos ao enviar formulário
    document.querySelectorAll('.auto-save').forEach(function(form) {
        form.addEventListener('submit', function() {
            localStorage.removeItem('form_' + form.id);
        });
    });
});

// Funções utilitárias globais
window.utils = {
    formatCurrency: function(value) {
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        }).format(value);
    },

    formatDate: function(date) {
        return new Intl.DateTimeFormat('pt-BR').format(new Date(date));
    },

    formatDateTime: function(date) {
        return new Intl.DateTimeFormat('pt-BR', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        }).format(new Date(date));
    },

    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    throttle: function(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
};



