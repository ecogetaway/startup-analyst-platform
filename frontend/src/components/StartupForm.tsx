import React, { useState } from 'react';
import { StartupInput } from '../types';

interface StartupFormProps {
  onSubmit: (data: StartupInput) => void;
}

const StartupForm: React.FC<StartupFormProps> = ({ onSubmit }) => {
  const [formData, setFormData] = useState<StartupInput>({
    company_name: '',
    business_description: '',
    industry: '',
    stage: '',
    founder_name: '',
    founder_background: '',
    website: '',
    pitch_deck_url: '',
    additional_info: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (formData.company_name && formData.business_description) {
      onSubmit(formData);
    }
  };

  const isFormValid = formData.company_name.trim() && formData.business_description.trim();

  return (
    <div className="card">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          📊 Analyze Your Startup
        </h2>
        <p className="text-gray-600">
          Provide details about your startup to get comprehensive AI-powered investment analysis
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <label htmlFor="company_name" className="block text-sm font-medium text-gray-700 mb-2">
              Company Name *
            </label>
            <input
              type="text"
              id="company_name"
              name="company_name"
              value={formData.company_name}
              onChange={handleChange}
              className="input-field"
              placeholder="Enter company name"
              required
            />
          </div>

          <div>
            <label htmlFor="industry" className="block text-sm font-medium text-gray-700 mb-2">
              Industry
            </label>
            <select
              id="industry"
              name="industry"
              value={formData.industry}
              onChange={handleChange}
              className="input-field"
            >
              <option value="">Select industry</option>
              <option value="Technology">Technology</option>
              <option value="Healthcare">Healthcare</option>
              <option value="Fintech">Fintech</option>
              <option value="E-commerce">E-commerce</option>
              <option value="SaaS">SaaS</option>
              <option value="AI/ML">AI/ML</option>
              <option value="Biotech">Biotech</option>
              <option value="CleanTech">CleanTech</option>
              <option value="EdTech">EdTech</option>
              <option value="Other">Other</option>
            </select>
          </div>
        </div>

        <div>
          <label htmlFor="business_description" className="block text-sm font-medium text-gray-700 mb-2">
            Business Description *
          </label>
          <textarea
            id="business_description"
            name="business_description"
            value={formData.business_description}
            onChange={handleChange}
            rows={4}
            className="input-field"
            placeholder="Describe your business, products/services, target market, and value proposition"
            required
          />
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <label htmlFor="stage" className="block text-sm font-medium text-gray-700 mb-2">
              Funding Stage
            </label>
            <select
              id="stage"
              name="stage"
              value={formData.stage}
              onChange={handleChange}
              className="input-field"
            >
              <option value="">Select stage</option>
              <option value="Pre-seed">Pre-seed</option>
              <option value="Seed">Seed</option>
              <option value="Series A">Series A</option>
              <option value="Series B">Series B</option>
              <option value="Series C+">Series C+</option>
              <option value="Growth">Growth</option>
            </select>
          </div>

          <div>
            <label htmlFor="founder_name" className="block text-sm font-medium text-gray-700 mb-2">
              Founder Name
            </label>
            <input
              type="text"
              id="founder_name"
              name="founder_name"
              value={formData.founder_name}
              onChange={handleChange}
              className="input-field"
              placeholder="Enter founder name"
            />
          </div>
        </div>

        <div>
          <label htmlFor="founder_background" className="block text-sm font-medium text-gray-700 mb-2">
            Founder Background
          </label>
          <textarea
            id="founder_background"
            name="founder_background"
            value={formData.founder_background}
            onChange={handleChange}
            rows={3}
            className="input-field"
            placeholder="Describe founder's experience, education, and relevant background"
          />
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <label htmlFor="website" className="block text-sm font-medium text-gray-700 mb-2">
              Website URL
            </label>
            <input
              type="url"
              id="website"
              name="website"
              value={formData.website}
              onChange={handleChange}
              className="input-field"
              placeholder="https://example.com"
            />
          </div>

          <div>
            <label htmlFor="pitch_deck_url" className="block text-sm font-medium text-gray-700 mb-2">
              Pitch Deck URL
            </label>
            <input
              type="url"
              id="pitch_deck_url"
              name="pitch_deck_url"
              value={formData.pitch_deck_url}
              onChange={handleChange}
              className="input-field"
              placeholder="https://example.com/pitch-deck"
            />
          </div>
        </div>

        <div>
          <label htmlFor="additional_info" className="block text-sm font-medium text-gray-700 mb-2">
            Additional Information
          </label>
          <textarea
            id="additional_info"
            name="additional_info"
            value={formData.additional_info}
            onChange={handleChange}
            rows={3}
            className="input-field"
            placeholder="Any additional information, metrics, partnerships, or context"
          />
        </div>

        <div className="flex justify-center pt-4">
          <button
            type="submit"
            disabled={!isFormValid}
            className={`px-8 py-3 rounded-lg font-medium transition-all duration-200 ${
              isFormValid
                ? 'btn-primary hover:shadow-lg transform hover:-translate-y-0.5'
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }`}
          >
            🚀 Analyze Startup
          </button>
        </div>
      </form>
    </div>
  );
};

export default StartupForm;
