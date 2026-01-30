/**
 * useChart - Chart.js configuration hook with theme support
 */

const useChart = () => {
  const chartColors = {
    primary: '#0A0E27',
    accent: '#00FF88',
    danger: '#FF3860',
    warning: '#FFB800',
    secondary: '#1A1F3A',
  };

  const getLineChartOptions = (title = '') => ({
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        labels: {
          color: '#ffffff',
          font: { family: "'Epilogue', sans-serif" },
        },
      },
      title: {
        display: !!title,
        text: title,
        color: '#ffffff',
        font: { family: "'Epilogue', sans-serif", size: 14 },
      },
    },
    scales: {
      x: {
        ticks: { color: '#ffffff' },
        grid: { color: 'rgba(255, 255, 255, 0.1)' },
      },
      y: {
        ticks: { color: '#ffffff' },
        grid: { color: 'rgba(255, 255, 255, 0.1)' },
      },
    },
  });

  const getBarChartOptions = (title = '') => ({
    ...getLineChartOptions(title),
    indexAxis: 'y',
  });

  const getPieChartOptions = (title = '') => ({
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        labels: {
          color: '#ffffff',
          font: { family: "'Epilogue', sans-serif" },
        },
      },
      title: {
        display: !!title,
        text: title,
        color: '#ffffff',
      },
    },
  });

  return {
    chartColors,
    getLineChartOptions,
    getBarChartOptions,
    getPieChartOptions,
  };
};

export default useChart;
