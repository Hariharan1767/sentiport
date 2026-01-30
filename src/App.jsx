import { useState } from 'react';
import Navigation from './components/Navigation';
import { ToastContainer } from './components/common';
import { useToast } from './hooks';

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const { toasts, removeToast } = useToast();

  const renderPage = () => {
    const pages = {
      dashboard: () => import('./components/Dashboard').then((m) => m.default),
      optimize: () => import('./components/Optimize').then((m) => m.default),
      analysis: () => import('./components/Analysis').then((m) => m.default),
      settings: () => import('./components/Settings').then((m) => m.default),
    };
    return pages[currentPage]?.();
  };

  const Page = currentPage === 'dashboard'
    ? () => {
      const Dashboard = require('./components/Dashboard').default;
      return <Dashboard />;
    }
    : currentPage === 'optimize'
      ? () => {
        const Optimize = require('./components/Optimize').default;
        return <Optimize />;
      }
      : currentPage === 'analysis'
        ? () => {
          const Analysis = require('./components/Analysis').default;
          return <Analysis />;
        }
        : () => {
          const Settings = require('./components/Settings').default;
          return <Settings />;
        };

  return (
    <div className="min-h-screen bg-primary text-white">
      <Navigation />
      <main className="container mx-auto px-4 py-8">
        <Page />
      </main>
      <ToastContainer toasts={toasts} onClose={removeToast} />
    </div>
  );
}

export default App;
