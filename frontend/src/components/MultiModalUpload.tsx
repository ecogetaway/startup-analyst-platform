import React, { useState, useCallback } from 'react';
import { 
  DocumentArrowUpIcon, 
  MicrophoneIcon, 
  VideoCameraIcon,
  CloudArrowUpIcon, 
  CheckCircleIcon,
  ExclamationTriangleIcon 
} from '@heroicons/react/24/outline';

interface UploadedFile {
  name: string;
  size: number;
  type: 'document' | 'audio' | 'video';
  public_url?: string;
  storage_path?: string;
  timestamp: number;
  processing_status?: 'pending' | 'processing' | 'completed' | 'failed';
}

interface MultiModalUploadProps {
  onFilesUploaded: (files: UploadedFile[]) => void;
  startupId?: string;
  disabled?: boolean;
}

const MultiModalUpload: React.FC<MultiModalUploadProps> = ({ 
  onFilesUploaded, 
  startupId, 
  disabled = false 
}) => {
  const [isDragging, setIsDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'all' | 'document' | 'audio' | 'video'>('all');

  const fileTypeConfig = {
    document: {
      extensions: ['.pdf', '.ppt', '.pptx', '.doc', '.docx', '.txt'],
      mimeTypes: ['application/pdf', 'application/vnd.ms-powerpoint', 
                  'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                  'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                  'text/plain'],
      icon: DocumentArrowUpIcon,
      label: 'Pitch Decks & Documents',
      description: 'PDF, PowerPoint, Word documents',
      color: 'blue',
      maxSize: 25 * 1024 * 1024 // 25MB
    },
    audio: {
      extensions: ['.mp3', '.wav', '.m4a', '.aac', '.flac', '.ogg'],
      mimeTypes: ['audio/mpeg', 'audio/wav', 'audio/x-m4a', 'audio/aac', 'audio/flac', 'audio/ogg'],
      icon: MicrophoneIcon,
      label: 'Voice Notes & Pitches',
      description: 'MP3, WAV, M4A audio files',
      color: 'green',
      maxSize: 50 * 1024 * 1024 // 50MB
    },
    video: {
      extensions: ['.mp4', '.mov', '.avi', '.mkv', '.webm'],
      mimeTypes: ['video/mp4', 'video/quicktime', 'video/x-msvideo', 'video/x-matroska', 'video/webm'],
      icon: VideoCameraIcon,
      label: 'Video Pitches',
      description: 'MP4, MOV, AVI video files',
      color: 'purple',
      maxSize: 100 * 1024 * 1024 // 100MB
    }
  };

  const detectFileType = (file: File): 'document' | 'audio' | 'video' => {
    const fileName = file.name.toLowerCase();
    const fileType = file.type.toLowerCase();

    for (const [type, config] of Object.entries(fileTypeConfig)) {
      if (config.extensions.some(ext => fileName.endsWith(ext)) ||
          config.mimeTypes.includes(fileType)) {
        return type as 'document' | 'audio' | 'video';
      }
    }
    
    return 'document'; // Default fallback
  };

  const validateFile = (file: File): { valid: boolean; error?: string } => {
    const fileType = detectFileType(file);
    const config = fileTypeConfig[fileType];

    if (file.size > config.maxSize) {
      return {
        valid: false,
        error: `${fileType} files must be smaller than ${Math.round(config.maxSize / (1024 * 1024))}MB`
      };
    }

    return { valid: true };
  };

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    if (!disabled) {
      setIsDragging(true);
    }
  }, [disabled]);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    if (disabled) return;

    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      handleMultipleFileUpload(files);
    }
  }, [disabled]);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (disabled) return;
    
    const files = e.target.files;
    if (files && files.length > 0) {
      handleMultipleFileUpload(Array.from(files));
    }
  };

  const handleMultipleFileUpload = async (files: File[]) => {
    setUploading(true);
    setUploadError(null);

    const uploadPromises = files.map(file => handleSingleFileUpload(file));
    
    try {
      const results = await Promise.allSettled(uploadPromises);
      
      const successfulUploads = results
        .filter((result): result is PromiseFulfilledResult<UploadedFile> => result.status === 'fulfilled')
        .map(result => result.value);
      
      const failedUploads = results
        .filter(result => result.status === 'rejected')
        .length;

      if (failedUploads > 0) {
        setUploadError(`${failedUploads} file(s) failed to upload`);
      }

      if (successfulUploads.length > 0) {
        setUploadedFiles(prev => [...prev, ...successfulUploads]);
        onFilesUploaded([...uploadedFiles, ...successfulUploads]);
      }
    } catch (error) {
      setUploadError('Upload failed. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  const handleSingleFileUpload = async (file: File): Promise<UploadedFile> => {
    // Validate file
    const validation = validateFile(file);
    if (!validation.valid) {
      throw new Error(validation.error);
    }

    const fileType = detectFileType(file);

    try {
      const formData = new FormData();
      formData.append('file', file);
      if (startupId) {
        formData.append('startup_id', startupId);
      }

      const response = await fetch('/api/upload-file', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`);
      }

      const result = await response.json();
      
      if (result.status === 'success') {
        return {
          name: file.name,
          size: result.size || file.size,
          type: fileType,
          public_url: result.public_url,
          storage_path: result.filename,
          timestamp: result.timestamp || Date.now(),
          processing_status: 'completed'
        };
      } else {
        throw new Error(result.detail || 'Upload failed');
      }
    } catch (error: any) {
      throw new Error(`Failed to upload ${file.name}: ${error.message}`);
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getFileIcon = (type: 'document' | 'audio' | 'video') => {
    const config = fileTypeConfig[type];
    const IconComponent = config.icon;
    const colorClass = {
      blue: 'text-blue-500',
      green: 'text-green-500',
      purple: 'text-purple-500'
    }[config.color];
    
    return <IconComponent className={`h-5 w-5 ${colorClass}`} />;
  };

  const filteredFiles = activeTab === 'all' 
    ? uploadedFiles 
    : uploadedFiles.filter(file => file.type === activeTab);

  return (
    <div className="space-y-6">
      {/* Multi-Modal Upload Area */}
      <div
        className={`
          relative border-2 border-dashed rounded-lg p-8 transition-colors duration-200
          ${isDragging 
            ? 'border-blue-400 bg-blue-50' 
            : 'border-gray-300 hover:border-gray-400'
          }
          ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
          ${uploading ? 'pointer-events-none' : ''}
        `}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <input
          type="file"
          accept={Object.values(fileTypeConfig).flatMap(config => 
            [...config.extensions, ...config.mimeTypes]
          ).join(',')}
          onChange={handleFileSelect}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          disabled={disabled || uploading}
          multiple
          id="multimodal-file-upload"
        />
        
        <div className="text-center">
          {uploading ? (
            <>
              <CloudArrowUpIcon className="mx-auto h-16 w-16 text-blue-500 animate-pulse" />
              <p className="mt-4 text-lg font-medium text-gray-900">Processing uploads...</p>
              <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                <div className="bg-blue-600 h-2 rounded-full animate-pulse" style={{ width: '60%' }}></div>
              </div>
            </>
          ) : (
            <>
              <div className="flex justify-center space-x-4 mb-4">
                <DocumentArrowUpIcon className="h-12 w-12 text-blue-400" />
                <MicrophoneIcon className="h-12 w-12 text-green-400" />
                <VideoCameraIcon className="h-12 w-12 text-purple-400" />
              </div>
              <p className="text-lg font-medium text-gray-900">
                Multi-Modal Pitch Upload
              </p>
              <p className="mt-2 text-sm text-gray-600">
                <span className="font-medium text-blue-600">Click to upload</span> or drag and drop
              </p>
              <p className="text-xs text-gray-500 mt-1">
                Support for documents, audio recordings, and video pitches
              </p>
            </>
          )}
        </div>
      </div>

      {/* File Type Information */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {Object.entries(fileTypeConfig).map(([type, config]) => {
          const IconComponent = config.icon;
          const bgColorClass = {
            blue: 'bg-blue-50 border-blue-200',
            green: 'bg-green-50 border-green-200',
            purple: 'bg-purple-50 border-purple-200'
          }[config.color];
          const textColorClass = {
            blue: 'text-blue-800',
            green: 'text-green-800',
            purple: 'text-purple-800'
          }[config.color];

          return (
            <div key={type} className={`border rounded-lg p-4 ${bgColorClass}`}>
              <div className="flex items-center space-x-3">
                <IconComponent className={`h-6 w-6 ${textColorClass}`} />
                <div>
                  <h4 className={`text-sm font-medium ${textColorClass}`}>
                    {config.label}
                  </h4>
                  <p className={`text-xs ${textColorClass} opacity-75`}>
                    {config.description}
                  </p>
                  <p className={`text-xs ${textColorClass} opacity-60 mt-1`}>
                    Max: {Math.round(config.maxSize / (1024 * 1024))}MB
                  </p>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Upload Error */}
      {uploadError && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <ExclamationTriangleIcon className="h-5 w-5 text-red-400" />
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-800">{uploadError}</p>
            </div>
          </div>
        </div>
      )}

      {/* Uploaded Files */}
      {uploadedFiles.length > 0 && (
        <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200">
            <h4 className="text-lg font-medium text-gray-900">Uploaded Pitch Materials</h4>
            <p className="text-sm text-gray-600 mt-1">
              {uploadedFiles.length} file(s) ready for multi-modal analysis
            </p>
          </div>

          {/* File Type Tabs */}
          <div className="px-6 pt-4">
            <div className="flex space-x-1">
              {['all', 'document', 'audio', 'video'].map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab as typeof activeTab)}
                  className={`px-3 py-2 text-xs font-medium rounded-md transition-colors ${
                    activeTab === tab
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  {tab === 'all' ? 'All Files' : `${tab.charAt(0).toUpperCase() + tab.slice(1)}s`}
                  {tab !== 'all' && (
                    <span className="ml-1 text-xs">
                      ({uploadedFiles.filter(f => f.type === tab).length})
                    </span>
                  )}
                </button>
              ))}
            </div>
          </div>

          {/* Files List */}
          <div className="px-6 py-4 space-y-3">
            {filteredFiles.map((file, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-md">
                <div className="flex items-center space-x-3">
                  {getFileIcon(file.type)}
                  <div>
                    <p className="text-sm font-medium text-gray-900">{file.name}</p>
                    <div className="flex items-center space-x-2 text-xs text-gray-500">
                      <span>{formatFileSize(file.size)}</span>
                      <span>•</span>
                      <span className="capitalize">{file.type}</span>
                      {file.processing_status === 'completed' && (
                        <>
                          <span>•</span>
                          <span className="text-green-600 flex items-center">
                            <CheckCircleIcon className="h-3 w-3 mr-1" />
                            Processed
                          </span>
                        </>
                      )}
                    </div>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  {file.public_url && (
                    <a
                      href={file.public_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-xs text-blue-600 hover:text-blue-800"
                    >
                      View
                    </a>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Multi-Modal Processing Info */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-lg p-4">
        <h4 className="text-sm font-medium text-blue-900 mb-2">🚀 Advanced Multi-Modal Analysis</h4>
        <ul className="text-xs text-blue-800 space-y-1">
          <li>• <strong>Documents:</strong> Extract structured content, financial data, and key metrics</li>
          <li>• <strong>Audio:</strong> Speech-to-text, presentation quality, and message clarity analysis</li>
          <li>• <strong>Video:</strong> Visual presentation analysis, speaker assessment, and content quality</li>
          <li>• <strong>AI Integration:</strong> Gemini AI synthesizes insights across all formats</li>
          <li>• <strong>Deal Memo:</strong> Generate professional investment memos automatically</li>
        </ul>
      </div>
    </div>
  );
};

export default MultiModalUpload;
