/* ========================================
   MODAL SYSTEM - Base Modal Class
   ======================================== */

class BaseModal {
  constructor(options = {}) {
    this.id = options.id || `modal-${Math.random().toString(36).substr(2, 9)}`;
    this.title = options.title || '';
    this.type = options.type || 'default'; // default, error, success, warning
    this.size = options.size || 'md'; // sm, md, lg
    this.onConfirm = options.onConfirm || null;
    this.onCancel = options.onCancel || null;
    this.overlay = null;
    this.element = null;
    this.init();
  }

  init() {
    this.createModal();
  }

  createModal() {
    // Create overlay
    this.overlay = document.createElement('div');
    this.overlay.className = 'modal-overlay';
    this.overlay.id = `overlay-${this.id}`;
    this.overlay.addEventListener('click', (e) => {
      if (e.target === this.overlay) {
        this.close();
      }
    });

    // Create modal
    this.element = document.createElement('div');
    this.element.className = `modal ${this.type}`;
    this.element.id = this.id;

    // Modal header
    const header = document.createElement('div');
    header.className = 'modal-header';
    header.innerHTML = `
      <h2 class="modal-title">${this.title}</h2>
      <button class="modal-close-btn" aria-label="Close">&times;</button>
    `;
    header.querySelector('.modal-close-btn').addEventListener('click', () => this.close());

    // Modal body
    const body = document.createElement('div');
    body.className = 'modal-body';
    body.id = `${this.id}-body`;

    // Modal footer
    const footer = document.createElement('div');
    footer.className = 'modal-footer';
    footer.id = `${this.id}-footer`;

    this.element.appendChild(header);
    this.element.appendChild(body);
    this.element.appendChild(footer);

    document.body.appendChild(this.overlay);
    this.overlay.appendChild(this.element);
  }

  setContent(htmlContent) {
    const body = this.element.querySelector(`#${this.id}-body`);
    body.innerHTML = htmlContent;
    return this;
  }

  setFooter(htmlContent) {
    const footer = this.element.querySelector(`#${this.id}-footer`);
    footer.innerHTML = htmlContent;
    return this;
  }

  open() {
    this.overlay.classList.add('show');
    document.body.style.overflow = 'hidden';
  }

  close() {
    this.overlay.classList.remove('show');
    document.body.style.overflow = 'auto';
    if (this.onCancel) {
      this.onCancel();
    }
  }

  destroy() {
    this.overlay.remove();
    this.overlay = null;
    this.element = null;
  }

  confirm() {
    if (this.onConfirm) {
      this.onConfirm();
    }
    this.close();
  }
}

/* ========================================
   EDIT/CREATE MODAL
   ======================================== */

class EditCreateModal extends BaseModal {
  constructor(options = {}) {
    options.type = 'default';
    super(options);
    this.formFields = options.fields || [];
    this.isEditMode = options.isEditMode || false;
    this.data = options.data || {};
    this.setupForm();
  }

  setupForm() {
    let formHTML = '<form id="edit-create-form" class="edit-create-form">';

    this.formFields.forEach((field) => {
      const value = this.data[field.name] || '';
      formHTML += `
        <div class="form-group">
          <label for="${field.name}">${field.label}</label>
          ${this.createInputField(field, value)}
        </div>
      `;
    });

    formHTML += '</form>';
    this.setContent(formHTML);

    // Add footer buttons
    const footerHTML = `
      <button class="btn btn-secondary" id="cancel-btn">Cancel</button>
      <button class="btn btn-primary" id="submit-btn">${this.isEditMode ? 'Update' : 'Create'}</button>
    `;
    this.setFooter(footerHTML);

    // Attach event listeners
    this.element.querySelector('#cancel-btn').addEventListener('click', () => this.close());
    this.element.querySelector('#submit-btn').addEventListener('click', () => this.submitForm());
  }

  createInputField(field, value) {
    const { name, type = 'text', placeholder = '', required = false, options = [] } = field;
    const requiredAttr = required ? 'required' : '';

    if (type === 'textarea') {
      return `<textarea class="form-control" name="${name}" id="${name}" placeholder="${placeholder}" ${requiredAttr}>${value}</textarea>`;
    }

    if (type === 'select') {
      let selectHTML = `<select class="form-control" name="${name}" id="${name}" ${requiredAttr}>`;
      selectHTML += `<option value="">-- Select --</option>`;
      options.forEach((opt) => {
        const selected = opt.value === value ? 'selected' : '';
        selectHTML += `<option value="${opt.value}" ${selected}>${opt.label}</option>`;
      });
      selectHTML += '</select>';
      return selectHTML;
    }

    return `<input type="${type}" class="form-control" name="${name}" id="${name}" placeholder="${placeholder}" value="${value}" ${requiredAttr} />`;
  }

  getFormData() {
    const form = this.element.querySelector('#edit-create-form');
    const formData = new FormData(form);
    const data = {};
    formData.forEach((value, key) => {
      data[key] = value;
    });
    return data;
  }

  submitForm() {
    const form = this.element.querySelector('#edit-create-form');
    if (form.checkValidity() === false) {
      form.reportValidity();
      return;
    }

    const formData = this.getFormData();
    if (this.onConfirm) {
      this.onConfirm(formData);
    }
    this.close();
  }
}

/* ========================================
   ERROR MODAL
   ======================================== */

class ErrorModal extends BaseModal {
  constructor(options = {}) {
    options.type = 'error';
    options.title = options.title || 'Error';
    super(options);
    this.message = options.message || 'An error occurred. Please try again.';
    this.setupError();
  }

  setupError() {
    const errorHTML = `
      <div class="alert alert-danger">
        <span>${this.message}</span>
      </div>
    `;
    this.setContent(errorHTML);

    const footerHTML = `<button class="btn btn-danger" id="error-close-btn">Close</button>`;
    this.setFooter(footerHTML);

    this.element.querySelector('#error-close-btn').addEventListener('click', () => this.close());
  }

  setMessage(message) {
    this.message = message;
    const errorHTML = `
      <div class="alert alert-danger">
        <span>${this.message}</span>
      </div>
    `;
    this.setContent(errorHTML);
    return this;
  }
}

/* ========================================
   DIALOGUE MODAL
   ======================================== */

class DialogueModal extends BaseModal {
  constructor(options = {}) {
    options.type = 'default';
    super(options);
    this.message = options.message || '';
    this.confirmText = options.confirmText || 'Confirm';
    this.cancelText = options.cancelText || 'Cancel';
    this.isDangerous = options.isDangerous || false;
    this.setupDialogue();
  }

  setupDialogue() {
    const dialogueHTML = `<p>${this.message}</p>`;
    this.setContent(dialogueHTML);

    const confirmBtnClass = this.isDangerous ? 'btn btn-danger' : 'btn btn-primary';
    const footerHTML = `
      <button class="btn btn-secondary" id="dialogue-cancel-btn">${this.cancelText}</button>
      <button class="${confirmBtnClass}" id="dialogue-confirm-btn">${this.confirmText}</button>
    `;
    this.setFooter(footerHTML);

    this.element.querySelector('#dialogue-cancel-btn').addEventListener('click', () => this.close());
    this.element.querySelector('#dialogue-confirm-btn').addEventListener('click', () => this.confirm());
  }
}

/* ========================================
   PRELOADER
   ======================================== */

class Preloader {
  constructor() {
    this.element = null;
    this.init();
  }

  init() {
    this.element = document.createElement('div');
    this.element.className = 'preloader';
    this.element.id = 'app-preloader';
    this.element.innerHTML = '<div class="spinner"></div>';
    document.body.appendChild(this.element);
  }

  show() {
    if (this.element) {
      this.element.classList.add('show');
    }
  }

  hide() {
    if (this.element) {
      this.element.classList.remove('show');
    }
  }

  setSize(size) {
    const spinner = this.element.querySelector('.spinner');
    if (size === 'lg') {
      spinner.classList.add('spinner-lg');
    } else {
      spinner.classList.remove('spinner-lg');
    }
    return this;
  }
}

/* ========================================
   GLOBAL INSTANCES & UTILITIES
   ======================================== */

// Create global preloader instance
const preloader = new Preloader();

// Utility function to show error modal
function showError(message, title = 'Error') {
  const errorModal = new ErrorModal({
    title: title,
    message: message,
  });
  errorModal.open();
}

// Utility function to show confirmation dialog
function showConfirm(message, onConfirm, options = {}) {
  const dialogueModal = new DialogueModal({
    title: options.title || 'Confirmation',
    message: message,
    confirmText: options.confirmText || 'Confirm',
    cancelText: options.cancelText || 'Cancel',
    isDangerous: options.isDangerous || false,
    onConfirm: onConfirm,
  });
  dialogueModal.open();
  return dialogueModal;
}

// Utility function to show edit/create form
function showEditCreateForm(fields, onSubmit, options = {}) {
  const modal = new EditCreateModal({
    title: options.title || (options.isEditMode ? 'Edit' : 'Create'),
    fields: fields,
    data: options.data || {},
    isEditMode: options.isEditMode || false,
    onConfirm: onSubmit,
  });
  modal.open();
  return modal;
}

/* ========================================
   EXPORT FOR USE IN MODULES
   ======================================== */

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    BaseModal,
    EditCreateModal,
    ErrorModal,
    DialogueModal,
    Preloader,
    preloader,
    showError,
    showConfirm,
    showEditCreateForm,
  };
}
