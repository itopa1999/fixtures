/* ========================================
   PARTICLE SYSTEM - Modern Visual Effects
   ======================================== */

class ParticleSystem {
    constructor(containerId, particleCount = 50) {
        this.container = document.getElementById(containerId);
        this.particles = [];
        this.particleCount = particleCount;
        this.init();
    }

    init() {
        for (let i = 0; i < this.particleCount; i++) {
            this.createParticle();
        }
    }

    createParticle() {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        const size = Math.random() * 3 + 1;
        const x = Math.random() * window.innerWidth;
        const y = Math.random() * window.innerHeight;
        const duration = Math.random() * 20 + 15;
        const delay = Math.random() * 5;
        
        particle.style.width = size + 'px';
        particle.style.height = size + 'px';
        particle.style.left = x + 'px';
        particle.style.top = y + 'px';
        particle.style.opacity = Math.random() * 0.5 + 0.2;
        particle.style.animation = `float ${duration}s linear ${delay}s infinite`;
        
        this.container.appendChild(particle);
        this.particles.push({
            element: particle,
            x: x,
            y: y,
            size: size,
            vx: (Math.random() - 0.5) * 0.5,
            vy: (Math.random() - 0.5) * 0.5
        });
    }

    animateParticles() {
        const animate = () => {
            this.particles.forEach(p => {
                p.x += p.vx;
                p.y += p.vy;
                
                // Bounce off edges
                if (p.x < 0 || p.x > window.innerWidth) p.vx *= -1;
                if (p.y < 0 || p.y > window.innerHeight) p.vy *= -1;
                
                // Wrap around
                if (p.x < -50) p.x = window.innerWidth + 50;
                if (p.x > window.innerWidth + 50) p.x = -50;
                if (p.y < -50) p.y = window.innerHeight + 50;
                if (p.y > window.innerHeight + 50) p.y = -50;
                
                p.element.style.transform = `translate(${p.x}px, ${p.y}px)`;
            });
            
            requestAnimationFrame(animate);
        };
        
        animate();
    }
}

// Add float animation to CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes float {
        0% { transform: translateY(0px) translateX(0px); }
        25% { transform: translateY(-50px) translateX(50px); }
        50% { transform: translateY(-100px) translateX(0px); }
        75% { transform: translateY(-50px) translateX(-50px); }
        100% { transform: translateY(0px) translateX(0px); }
    }
`;
document.head.appendChild(style);

// Initialize particles when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const particlesContainer = document.getElementById('particles');
    if (particlesContainer) {
        const particleSystem = new ParticleSystem('particles', 40);
        particleSystem.animateParticles();
    }
});
