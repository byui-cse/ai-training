// Auction House Frontend JavaScript

class AuctionApp {
  constructor() {
    this.apiBase = 'http://localhost:8000';
    this.currentUser = null;
    this.auctions = [];
    this.currentPage = 0;
    this.pageSize = 12;

    this.init();
  }

  init() {
    this.bindEvents();
    this.loadAuctions();
    this.checkAuthStatus();
  }

  bindEvents() {
    // Navigation
    document.getElementById('loginBtn').addEventListener('click', () => this.showModal('login'));
    document.getElementById('registerBtn').addEventListener('click', () => this.showModal('register'));

    // Modal close
    document.querySelectorAll('.modal-close').forEach(close => {
      close.addEventListener('click', () => this.hideModals());
    });

    // Click outside modal
    document.querySelectorAll('.modal').forEach(modal => {
      modal.addEventListener('click', (e) => {
        if (e.target === modal) this.hideModals();
      });
    });

    // Forms
    document.getElementById('loginForm').addEventListener('submit', (e) => this.handleLogin(e));
    document.getElementById('registerForm').addEventListener('submit', (e) => this.handleRegister(e));

    // Load more auctions
    document.getElementById('loadMoreBtn').addEventListener('click', () => this.loadMoreAuctions());
  }

  showModal(type) {
    this.hideModals();
    const modalId = type === 'login' ? 'loginModal' : 'registerModal';
    document.getElementById(modalId).style.display = 'block';
  }

  hideModals() {
    document.querySelectorAll('.modal').forEach(modal => {
      modal.style.display = 'none';
    });
  }

  async handleLogin(e) {
    e.preventDefault();
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

    try {
      const response = await fetch(`${this.apiBase}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          username: username,
          password: password
        })
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.access_token);
        this.currentUser = { username };
        this.updateUIForAuth();
        this.hideModals();
        this.showNotification('Login successful!', 'success');
      } else {
        const error = await response.json();
        this.showNotification(error.detail || 'Login failed', 'error');
      }
    } catch (error) {
      this.showNotification('Network error. Please try again.', 'error');
    }
  }

  async handleRegister(e) {
    e.preventDefault();
    const username = document.getElementById('registerUsername').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;

    try {
      const response = await fetch(`${this.apiBase}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: username,
          email: email,
          password: password
        })
      });

      if (response.ok) {
        this.showNotification('Registration successful! Please login.', 'success');
        this.hideModals();
        // Switch to login modal
        setTimeout(() => this.showModal('login'), 1000);
      } else {
        const error = await response.json();
        this.showNotification(error.detail || 'Registration failed', 'error');
      }
    } catch (error) {
      this.showNotification('Network error. Please try again.', 'error');
    }
  }

  async loadAuctions(activeOnly = false) {
    try {
      const params = new URLSearchParams({
        skip: this.currentPage * this.pageSize,
        limit: this.pageSize
      });

      if (activeOnly) {
        params.append('active_only', 'true');
      }

      const response = await fetch(`${this.apiBase}/items/?${params}`);
      if (response.ok) {
        const auctions = await response.json();
        this.auctions = [...this.auctions, ...auctions];
        this.renderAuctions(auctions);
      }
    } catch (error) {
      console.error('Error loading auctions:', error);
    }
  }

  async loadMoreAuctions() {
    this.currentPage++;
    await this.loadAuctions();
  }

  renderAuctions(auctions) {
    const grid = document.getElementById('auctionsGrid');

    auctions.forEach(auction => {
      const card = this.createAuctionCard(auction);
      grid.appendChild(card);
    });
  }

  createAuctionCard(auction) {
    const card = document.createElement('div');
    card.className = 'auction-card';

    const statusClass = `status-${auction.status.toLowerCase()}`;
    const statusText = auction.status.charAt(0).toUpperCase() + auction.status.slice(1);

    card.innerHTML = `
            <div class="auction-image">
                ${auction.image_url ? `<img src="${auction.image_url}" alt="${auction.title}">` : '🏷️'}
            </div>
            <div class="auction-content">
                <h3 class="auction-title">${auction.title}</h3>
                <p class="auction-description">${auction.description || 'No description available'}</p>
                <div class="auction-meta">
                    <div class="auction-price">$${auction.current_price.toFixed(2)}</div>
                    <span class="status-badge ${statusClass}">${statusText}</span>
                </div>
                <div class="auction-time">
                    Ends: ${new Date(auction.end_time).toLocaleDateString()}
                </div>
                <div class="auction-actions">
                    <button class="btn btn-primary" onclick="app.viewAuction(${auction.id})">
                        View Details
                    </button>
                    ${this.currentUser && auction.status === 'active' ?
        `<button class="btn btn-outline" onclick="app.placeBid(${auction.id})">
                            Place Bid
                        </button>` : ''}
                </div>
            </div>
        `;

    return card;
  }

  checkAuthStatus() {
    const token = localStorage.getItem('token');
    if (token) {
      // In a real app, you'd validate the token with the server
      this.currentUser = { username: 'user' }; // Simplified
      this.updateUIForAuth();
    }
  }

  updateUIForAuth() {
    const loginBtn = document.getElementById('loginBtn');
    const registerBtn = document.getElementById('registerBtn');

    if (this.currentUser) {
      loginBtn.textContent = 'Logout';
      loginBtn.onclick = () => this.logout();
      registerBtn.style.display = 'none';
    } else {
      loginBtn.textContent = 'Login';
      loginBtn.onclick = () => this.showModal('login');
      registerBtn.style.display = 'inline-block';
    }
  }

  logout() {
    localStorage.removeItem('token');
    this.currentUser = null;
    this.updateUIForAuth();
    this.showNotification('Logged out successfully', 'success');
  }

  showNotification(message, type = 'info') {
    // Simple notification - in a real app, you'd use a proper notification library
    alert(`${type.toUpperCase()}: ${message}`);
  }

  // Placeholder methods for future implementation
  viewAuction(id) {
    this.showNotification(`View auction ${id} - Feature coming soon!`, 'info');
  }

  placeBid(id) {
    this.showNotification(`Place bid on auction ${id} - Feature coming soon!`, 'info');
  }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  window.app = new AuctionApp();
});
