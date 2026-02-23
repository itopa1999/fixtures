/* ========================================
   COOKIE MANAGEMENT
   ======================================== */

/**
 * Get cookie value by name
 */
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

// Set global variables from cookies
window.userAccess = getCookie('access');
window.userRefresh = getCookie('refresh');
window.userEmail = getCookie('email');
window.userName = getCookie('name');
window.userGroups = getCookie('group');

/* ========================================
   OVERLAY STACK MANAGER - Track open modals/preloaders
   ======================================== */

class OverlayManager {
  constructor() {
    this.overlayCount = 0;
  }

  incrementOverlay() {
    this.overlayCount++;
    if (this.overlayCount === 1) {
      // First overlay opened - disable body interactions
      document.body.style.pointerEvents = 'none';
      document.body.style.overflow = 'hidden';
    }
  }

  decrementOverlay() {
    this.overlayCount--;
    if (this.overlayCount <= 0) {
      // All overlays closed - re-enable body interactions
      this.overlayCount = 0;
      document.body.style.pointerEvents = 'auto';
      document.body.style.overflow = 'auto';
    }
  }

  isActive() {
    return this.overlayCount > 0;
  }
}

const overlayManager = new OverlayManager();

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
    
    // Prevent all interactions outside the modal (don't close on overlay click)
    this.overlay.addEventListener('click', (e) => {
      e.stopPropagation();
      // Don't close the modal when clicking overlay
    });
    
    // Prevent scroll and interactions on body when modal is open
    this.overlay.addEventListener('wheel', (e) => {
      e.preventDefault();
    }, { passive: false });
    
    this.overlay.addEventListener('touchmove', (e) => {
      e.preventDefault();
    }, { passive: false });

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
    
    // Use overlay manager to track open overlays
    overlayManager.incrementOverlay();
    
    // Ensure overlay and modal are always interactive
    this.overlay.style.pointerEvents = 'auto';
    this.element.style.pointerEvents = 'auto';
    
    // Close on ESC key
    this.escHandler = (e) => {
      if (e.key === 'Escape') {
        this.close();
      }
    };
    document.addEventListener('keydown', this.escHandler);
  }

  close() {
    this.overlay.classList.remove('show');
    
    // Use overlay manager to track open overlays
    overlayManager.decrementOverlay();
    
    // Remove ESC handler
    if (this.escHandler) {
      document.removeEventListener('keydown', this.escHandler);
      this.escHandler = null;
    }
    
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
    // Keep modal open - don't close automatically (user closes or page redirects)
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
    this.isVisible = false;
    this.init();
  }

  init() {
    this.element = document.createElement('div');
    this.element.className = 'preloader';
    this.element.id = 'app-preloader';
    this.element.innerHTML = '<div class="spinner"></div>';
    
    // Prevent interactions while preloader is active
    this.element.addEventListener('click', (e) => {
      e.stopPropagation();
    });
    
    this.element.addEventListener('wheel', (e) => {
      e.preventDefault();
    }, { passive: false });
    
    this.element.addEventListener('touchmove', (e) => {
      e.preventDefault();
    }, { passive: false });
    
    document.body.appendChild(this.element);
  }

  show() {
    if (this.element && !this.isVisible) {
      this.element.classList.add('show');
      this.isVisible = true;
      
      // Use overlay manager to track open overlays
      overlayManager.incrementOverlay();
      
      // Ensure preloader is always interactive
      this.element.style.pointerEvents = 'auto';
    }
  }

  hide() {
    if (this.element && this.isVisible) {
      this.element.classList.remove('show');
      this.isVisible = false;
      
      // Use overlay manager to track open overlays
      overlayManager.decrementOverlay();
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

/* ========================================
   MAIN BASEURL DECLARATION
   ======================================== */

window.BASE_URL = null;
window.ADMIN_URL = "http://127.0.0.1:8000/api/admin/";

/* ========================================
   SIDEBAR NAVIGATION SYSTEM - Dynamic menu and page highlighting
   ======================================== */

class SidebarNavigation {
  constructor() {
    this.pages = [
      { name: 'Dashboard', icon: '📊', path: 'dashboard.html', id: 'dashboard' },
      { name: 'Tournaments', icon: '🏆', path: 'tournaments.html', id: 'tournaments' },
      { name: 'Players', icon: '👥', path: 'players.html', id: 'players' },
      { name: 'Matches', icon: '🎮', path: 'matches.html', id: 'matches' },
      { name: 'Brackets', icon: '📋', path: 'brackets.html', id: 'brackets' },
      { name: 'Reports', icon: '📊', path: 'reports.html', id: 'reports' },
    ];

    this.init();
  }

  init() {
    document.addEventListener('DOMContentLoaded', () => {
      this.renderMenu();
      this.highlightCurrentPage();
      this.setupMobileSidebar();
    });
  }

  renderMenu() {
    const sidebarNav = document.getElementById('sidebarNav');
    if (!sidebarNav) return;

    sidebarNav.innerHTML = '';

    this.pages.forEach(page => {
      const li = document.createElement('li');
      li.className = 'sidebar-nav-item';
      li.innerHTML = `
        <a href="${page.path}" class="sidebar-nav-link" data-page="${page.id}">
          <span class="sidebar-nav-icon">${page.icon}</span>
          <span class="sidebar-nav-label">${page.name}</span>
        </a>
      `;
      sidebarNav.appendChild(li);
    });
  }

  highlightCurrentPage() {
    const currentPage = this.getCurrentPageId();
    const navLinks = document.querySelectorAll('.sidebar-nav-link');

    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('data-page') === currentPage) {
        link.classList.add('active');
      }
    });
  }

  getCurrentPageId() {
    const path = window.location.pathname;
    const filename = path.split('/').pop() || 'dashboard.html';
    
    // Extract page ID from filename
    if (filename.includes('dashboard')) return 'dashboard';
    if (filename.includes('tournament')) return 'tournaments';
    if (filename.includes('player')) return 'players';
    if (filename.includes('match')) return 'matches';
    if (filename.includes('bracket')) return 'brackets';
    if (filename.includes('report')) return 'reports';
    
    return 'dashboard'; // Default
  }

  setupMobileSidebar() {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebarOverlay = document.getElementById('sidebarOverlay');

    if (!sidebarToggle || !sidebar) return;

    // Toggle sidebar on mobile
    sidebarToggle.addEventListener('click', () => {
      sidebar.classList.toggle('mobile-open');
      sidebarOverlay.classList.toggle('mobile-open');
    });

    // Close sidebar when clicking overlay
    if (sidebarOverlay) {
      sidebarOverlay.addEventListener('click', () => {
        sidebar.classList.remove('mobile-open');
        sidebarOverlay.classList.remove('mobile-open');
      });
    }

    // Close sidebar when clicking a nav link
    const navLinks = document.querySelectorAll('.sidebar-nav-link');
    navLinks.forEach(link => {
      link.addEventListener('click', () => {
        // Only close on mobile
        if (window.innerWidth <= 768) {
          sidebar.classList.remove('mobile-open');
          sidebarOverlay.classList.remove('mobile-open');
        }
      });
    });

    // Close sidebar when window is resized
    window.addEventListener('resize', () => {
      if (window.innerWidth > 768) {
        sidebar.classList.remove('mobile-open');
        sidebarOverlay.classList.remove('mobile-open');
      }
    });
  }
}

// Initialize sidebar navigation
const sidebarNav = new SidebarNavigation();

/* ========================================
   PAGE LOAD HANDLER - Hide preloader when page is ready
   ======================================== */

window.addEventListener('load', () => {
  // Hide preloader after page has fully loaded
  if (typeof preloader !== 'undefined') {
    preloader.hide();
  }
});

// Also hide preloader on DOMContentLoaded as fallback
document.addEventListener('DOMContentLoaded', () => {
  // Slight delay to ensure all resources are loaded
  setTimeout(() => {
    if (typeof preloader !== 'undefined' && preloader.isVisible) {
      preloader.hide();
    }
  }, 500);
});


