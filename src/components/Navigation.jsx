import { TrendingUp, Menu, X } from 'lucide-react';
import { useState } from 'react';

const Navigation = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const navLinks = ['Dashboard', 'Optimize', 'Analysis', 'Settings'];

  return (
    <nav className="glass-nav sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        {/* Logo */}
        <div className="flex items-center gap-2">
          <div className="bg-gradient-to-r from-accent to-green-400 p-2 rounded-lg glow">
            <TrendingUp className="w-6 h-6 text-primary" />
          </div>
          <span className="text-xl font-bold">SentiPort</span>
        </div>

        {/* Desktop Links */}
        <div className="hidden md:flex items-center gap-8">
          {navLinks.map((link) => (
            <a
              key={link}
              href={`#${link.toLowerCase()}`}
              className="text-gray-300 hover:text-accent transition-smooth pb-1 border-b-2 border-transparent hover:border-accent"
            >
              {link}
            </a>
          ))}
        </div>

        {/* Mobile Menu Button */}
        <button
          type="button"
          className="md:hidden text-accent"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        >
          {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden glass-nav border-t border-accent/20 p-4">
          {navLinks.map((link) => (
            <a
              key={link}
              href={`#${link.toLowerCase()}`}
              className="block py-2 text-accent hover:text-green-300 transition-smooth"
            >
              {link}
            </a>
          ))}
        </div>
      )}
    </nav>
  );
};

export default Navigation;
