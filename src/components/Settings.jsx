import { Button, Card, Input } from './common';

const Settings = () => {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold mb-2">Settings</h1>
        <p className="text-gray-400">Manage your application preferences</p>
      </div>

      <Card title="Data Source Configuration">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-semibold mb-2">Data Provider</label>
            <select className="w-full p-2.5 rounded-lg bg-secondary border border-accent/20">
              <option>Yahoo Finance</option>
              <option>Alpha Vantage</option>
              <option>Custom API</option>
            </select>
          </div>
          <Input label="API Key" type="password" placeholder="Enter your API key" />
          <Button variant="secondary" className="w-full">
            Test Connection
          </Button>
        </div>
      </Card>

      <Card title="Model Settings">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-semibold mb-2">Sentiment Model</label>
            <select className="w-full p-2.5 rounded-lg bg-secondary border border-accent/20">
              <option>Logistic Regression</option>
              <option>Naive Bayes</option>
              <option>SVM</option>
            </select>
          </div>
          <Input label="Max Features (TF-IDF)" type="number" placeholder="5000" />
          <Button variant="secondary" className="w-full">
            Retrain Model
          </Button>
        </div>
      </Card>

      <Card title="Portfolio Settings">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-semibold mb-2">Rebalance Frequency</label>
            <select className="w-full p-2.5 rounded-lg bg-secondary border border-accent/20">
              <option>Daily</option>
              <option>Weekly</option>
              <option>Monthly</option>
              <option>Quarterly</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-semibold mb-2">Max Position Size: 30%</label>
            <input type="range" min="5" max="50" defaultValue="30" className="w-full" />
          </div>
        </div>
      </Card>

      <div className="flex gap-4">
        <Button size="lg" className="flex-1">
          Save Settings
        </Button>
        <Button variant="secondary" size="lg" className="flex-1">
          Reset to Defaults
        </Button>
      </div>
    </div>
  );
};

export default Settings;
