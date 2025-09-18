import React, { useState, useCallback, useRef, useEffect } from 'react';
import { uploadFileDemo } from '../services/demoApi';
import { 
  DocumentArrowUpIcon, 
  MicrophoneIcon, 
  VideoCameraIcon,
  CloudArrowUpIcon,   
  CheckCircleIcon,
  ExclamationTriangleIcon,
  XMarkIcon,
  ClipboardDocumentListIcon
} from '@heroicons/react/24/outline';

interface UploadedFile {
  id: string; // Add unique ID
  name: string;
  size: number;
  type: 'document' | 'audio' | 'video' | 'questionnaire';
  public_url?: string;
  storage_path?: string;
  timestamp: number;
  processing_status?: 'pending' | 'processing' | 'completed' | 'failed';
  upload_progress?: number; // Add progress tracking
  error_message?: string; // Add error tracking
}

interface MultiModalUploadProps {
  onFilesUploaded: (files: UploadedFile[]) => void;
  startupId?: string;
  disabled?: boolean;
  maxFiles?: number; // Add max files limit
}

const MultiModalUpload: React.FC<MultiModalUploadProps> = ({ 
  onFilesUploaded, 
  startupId, 
  disabled = false,
  maxFiles = 10
}) => {
  const [isDragging, setIsDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'all' | 'document' | 'audio' | 'video' | 'questionnaire'>('all');
  
  // Add refs for cleanup
  const abortControllersRef = useRef<Map<string, AbortController>>(new Map());
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Cleanup on unmount
  useEffect(() => {
    const controllers = abortControllersRef.current;
    return () => {
      controllers.forEach(controller => controller.abort());
      controllers.clear();
    };
  }, []);

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
      maxSize: 100 * 1024 * 1024 // 100MB
    },
    audio: {
      extensions: ['.mp3', '.wav', '.m4a', '.aac', '.flac', '.ogg'],
      mimeTypes: ['audio/mpeg', 'audio/wav', 'audio/x-m4a', 'audio/aac', 'audio/flac', 'audio/ogg'],
      icon: MicrophoneIcon,
      label: 'Voice Notes & Pitches',
      description: 'MP3, WAV, M4A audio files',
      color: 'green',
      maxSize: 100 * 1024 * 1024 // 100MB
    },
    video: {
      extensions: ['.mp4', '.mov', '.avi', '.mkv', '.webm'],
      mimeTypes: ['video/mp4', 'video/quicktime', 'video/x-msvideo', 'video/x-matroska', 'video/webm'],
      icon: VideoCameraIcon,
      label: 'Video Pitches',
      description: 'MP4, MOV, AVI video files',
      color: 'purple',
      maxSize: 250 * 1024 * 1024 // 250MB
    },
    questionnaire: {
      extensions: ['.json', '.csv', '.xlsx'],
      mimeTypes: ['application/json', 'text/csv', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'],
      icon: ClipboardDocumentListIcon,
      label: 'Google Form Questionnaires',
      description: 'JSON, CSV, Excel exports',
      color: 'teal',
      maxSize: 10 * 1024 * 1024 // 10MB
    }
  };

  const generateFileId = () => `file_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

  const detectFileType = (file: File): 'document' | 'audio' | 'video' | 'questionnaire' => {
    const fileName = file.name.toLowerCase();
    const fileType = file.type.toLowerCase();

    for (const [type, config] of Object.entries(fileTypeConfig)) {
      if (config.extensions.some(ext => fileName.endsWith(ext)) ||
          config.mimeTypes.includes(fileType)) {
        return type as 'document' | 'audio' | 'video' | 'questionnaire';
      }
    }
    
    return 'document'; // Default fallback
  };

  const validateFile = (file: File): { valid: boolean; error?: string } => {
    // Check if file already exists
    const isDuplicate = uploadedFiles.some(uploaded => 
      uploaded.name === file.name && uploaded.size === file.size
    );
    
    if (isDuplicate) {
      return {
        valid: false,
        error: `File "${file.name}" has already been uploaded`
      };
    }

    // Check max files limit
    if (uploadedFiles.length >= maxFiles) {
      return {
        valid: false,
        error: `Maximum ${maxFiles} files allowed`
      };
    }

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

  const handleMultipleFileUpload = useCallback(async (files: File[]) => {
    setUploading(true);
    setUploadError(null);

    // Pre-validate all files
    const validationResults = files.map(file => ({
      file,
      validation: validateFile(file)
    }));

    const validFiles = validationResults.filter(result => result.validation.valid);
    const invalidFiles = validationResults.filter(result => !result.validation.valid);

    // Show validation errors
    if (invalidFiles.length > 0) {
      const errorMessages = invalidFiles.map(result => 
        `${result.file.name}: ${result.validation.error}`
      ).join('\n');
      setUploadError(`Some files were rejected:\n${errorMessages}`);
    }

    if (validFiles.length === 0) {
      setUploading(false);
      return;
    }

    // Create pending file entries
    const pendingFiles: UploadedFile[] = validFiles.map(({ file }) => ({
      id: generateFileId(),
      name: file.name,
      size: file.size,
      type: detectFileType(file),
      timestamp: Date.now(),
      processing_status: 'pending',
      upload_progress: 0
    }));

    // Add pending files to state immediately
    setUploadedFiles(prev => {
      const newFiles = [...prev, ...pendingFiles];
      return newFiles;
    });

    // Upload files
    const uploadPromises = validFiles.map(({ file }, index) => 
      handleSingleFileUpload(file, pendingFiles[index].id)
    );
    
    try {
      const results = await Promise.allSettled(uploadPromises);
      
      const successfulUploads = results
        .filter((result): result is PromiseFulfilledResult<UploadedFile> => result.status === 'fulfilled')
        .map(result => result.value);
      
      const failedUploads = results
        .filter((result): result is PromiseRejectedResult => result.status === 'rejected')
        .map(result => result.reason);

      // Update state with final results
      setUploadedFiles(prev => {
        const updatedFiles = prev.map(file => {
          const successfulFile = successfulUploads.find(success => success.id === file.id);
          if (successfulFile) {
            return successfulFile;
          }
          
          const failedFile = failedUploads.find(error => error.message && error.message.includes(file.name));
          if (failedFile) {
            return {
              ...file,
              processing_status: 'failed' as const,
              error_message: failedFile.message
            };
          }
          
          return file;
        });
        
        // Notify parent of successful uploads only
        const completedFiles = updatedFiles.filter(f => f.processing_status === 'completed');
        onFilesUploaded(completedFiles);
        
        return updatedFiles;
      });

      if (failedUploads.length > 0) {
        const errorSummary = failedUploads.length === 1 
          ? failedUploads[0].message 
          : `${failedUploads.length} file(s) failed to upload`;
        setUploadError(errorSummary);
      }

    } catch (error) {
      setUploadError('Upload failed. Please try again.');
      console.error('Upload error:', error);
    } finally {
      setUploading(false);
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [onFilesUploaded]);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    if (disabled) return;

    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      handleMultipleFileUpload(files);
    }
  }, [disabled, handleMultipleFileUpload]);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (disabled) return;
    
    const files = e.target.files;
    if (files && files.length > 0) {
      handleMultipleFileUpload(Array.from(files));
    }
    
    // Reset input value to allow same file re-selection
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleSingleFileUpload = async (file: File, fileId: string): Promise<UploadedFile> => {
    const fileType = detectFileType(file);
    const abortController = new AbortController();
    abortControllersRef.current.set(fileId, abortController);

    try {
      // Update status to processing
      setUploadedFiles(prev => prev.map(f => 
        f.id === fileId 
          ? { ...f, processing_status: 'processing' as const, upload_progress: 10 }
          : f
      ));

      // Update progress to 50%
      setUploadedFiles(prev => prev.map(f => 
        f.id === fileId 
          ? { ...f, upload_progress: 50 }
          : f
      ));

      // Use demo API for Vercel deployment
      const result = await uploadFileDemo(file);

      // Update progress to 70%
      setUploadedFiles(prev => prev.map(f => 
        f.id === fileId 
          ? { ...f, upload_progress: 70 }
          : f
      ));
      
      // Final progress update
      setUploadedFiles(prev => prev.map(f => 
        f.id === fileId 
          ? { ...f, upload_progress: 100 }
          : f
      ));
      
      if (result.status === 'success') {
        const uploadedFile: UploadedFile = {
          id: fileId,
          name: file.name,
          size: result.size || file.size,
          type: fileType,
          public_url: result.public_url,
          storage_path: result.filename,
          timestamp: result.timestamp || Date.now(),
          processing_status: 'completed',
          upload_progress: 100
        };
        
        abortControllersRef.current.delete(fileId);
        return uploadedFile;
      } else {
        throw new Error('Upload failed');
      }
    } catch (error: any) {
      abortControllersRef.current.delete(fileId);
      if (error.name === 'AbortError') {
        throw new Error('Upload was cancelled');
      }
      throw new Error(`Failed to upload ${file.name}: ${error.message}`);
    }
  };

  const removeFile = (fileId: string) => {
    // Cancel upload if in progress
    const abortController = abortControllersRef.current.get(fileId);
    if (abortController) {
      abortController.abort();
      abortControllersRef.current.delete(fileId);
    }

    // Remove from state
    setUploadedFiles(prev => {
      const newFiles = prev.filter(f => f.id !== fileId);
      onFilesUploaded(newFiles.filter(f => f.processing_status === 'completed'));
      return newFiles;
    });
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getFileIcon = (type: 'document' | 'audio' | 'video' | 'questionnaire') => {
    const config = fileTypeConfig[type];
    const IconComponent = config.icon;
    const colorClass = {
      blue: 'text-blue-500',
      green: 'text-green-500',
      purple: 'text-purple-500',
      teal: 'text-teal-500'
    }[config.color];
    
    return <IconComponent className={`h-5 w-5 ${colorClass}`} />;
  };

  const filteredFiles = activeTab === 'all' 
    ? uploadedFiles 
    : uploadedFiles.filter(file => file.type === activeTab);

  const canUpload = !disabled && !uploading && uploadedFiles.length < maxFiles;

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
          ${!canUpload ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
        `}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept={Object.values(fileTypeConfig).flatMap(config => 
            [...config.extensions, ...config.mimeTypes]
          ).join(',')}
          onChange={handleFileSelect}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          disabled={!canUpload}
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
                <ClipboardDocumentListIcon className="h-12 w-12 text-teal-400" />
              </div>
              <p className="text-lg font-medium text-gray-900">
                Pitch Deck Upload
              </p>
              <p className="mt-2 text-sm text-gray-600">
                <span className="font-medium text-blue-600">Click to upload</span> or drag and drop your pitch deck
              </p>
              <p className="text-xs text-gray-500 mt-1">
                PDF, PowerPoint, audio, video, or Google Form questionnaires - Primary source for investment analysis
              </p>
              {uploadedFiles.length > 0 && (
                <p className="text-xs text-gray-400 mt-2">
                  {uploadedFiles.length}/{maxFiles} files uploaded
                </p>
              )}
            </>
          )}
        </div>
      </div>

      {/* File Type Information */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {Object.entries(fileTypeConfig).map(([type, config]) => {
          const IconComponent = config.icon;
          const bgColorClass = {
            blue: 'bg-blue-50 border-blue-200',
            green: 'bg-green-50 border-green-200',
            purple: 'bg-purple-50 border-purple-200',
            teal: 'bg-teal-50 border-teal-200'
          }[config.color];
          const textColorClass = {
            blue: 'text-blue-800',
            green: 'text-green-800',
            purple: 'text-purple-800',
            teal: 'text-teal-800'
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
          <div className="flex justify-between items-start">
            <div className="flex">
              <div className="flex-shrink-0">
                <ExclamationTriangleIcon className="h-5 w-5 text-red-400" />
              </div>
              <div className="ml-3">
                <p className="text-sm text-red-800 whitespace-pre-line">{uploadError}</p>
              </div>
            </div>
            <button
              onClick={() => setUploadError(null)}
              className="text-red-400 hover:text-red-600"
            >
              <XMarkIcon className="h-4 w-4" />
            </button>
          </div>
        </div>
      )}

      {/* Uploaded Files */}
      {uploadedFiles.length > 0 && (
        <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200">
            <h4 className="text-lg font-medium text-gray-900">Uploaded Pitch Deck</h4>
            <p className="text-sm text-gray-600 mt-1">
              {uploadedFiles.filter(f => f.processing_status === 'completed').length} of {uploadedFiles.length} file(s) ready for investment analysis
            </p>
          </div>

          {/* File Type Tabs */}
          <div className="px-6 pt-4">
            <div className="flex space-x-1">
              {['all', 'document', 'audio', 'video', 'questionnaire'].map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab as typeof activeTab)}
                  className={`px-3 py-2 text-xs font-medium rounded-md transition-colors ${
                    activeTab === tab
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  {tab === 'all' ? 'All Files' : 
                   tab === 'questionnaire' ? 'Questionnaires' :
                   `${tab.charAt(0).toUpperCase() + tab.slice(1)}s`}
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
            {filteredFiles.map((file) => (
              <div key={file.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-md">
                <div className="flex items-center space-x-3 flex-1">
                  {getFileIcon(file.type)}
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900">{file.name}</p>
                    <div className="flex items-center space-x-2 text-xs text-gray-500">
                      <span>{formatFileSize(file.size)}</span>
                      <span>•</span>
                      <span className="capitalize">{file.type}</span>
                      
                      {file.processing_status === 'pending' && (
                        <>
                          <span>•</span>
                          <span className="text-yellow-600">Pending...</span>
                        </>
                      )}
                      
                      {file.processing_status === 'processing' && (
                        <>
                          <span>•</span>
                          <span className="text-blue-600">Uploading {file.upload_progress}%</span>
                        </>
                      )}
                      
                      {file.processing_status === 'completed' && (
                        <>
                          <span>•</span>
                          <span className="text-green-600 flex items-center">
                            <CheckCircleIcon className="h-3 w-3 mr-1" />
                            Ready
                          </span>
                        </>
                      )}
                      
                      {file.processing_status === 'failed' && (
                        <>
                          <span>•</span>
                          <span className="text-red-600">Failed</span>
                        </>
                      )}
                    </div>
                    
                    {file.processing_status === 'processing' && file.upload_progress !== undefined && (
                      <div className="mt-1 w-full bg-gray-200 rounded-full h-1">
                        <div 
                          className="bg-blue-600 h-1 rounded-full transition-all duration-300" 
                          style={{ width: `${file.upload_progress}%` }}
                        ></div>
                      </div>
                    )}
                    
                    {file.error_message && (
                      <p className="text-xs text-red-600 mt-1">{file.error_message}</p>
                    )}
                  </div>
                </div>
                
                <div className="flex items-center space-x-2 ml-4">
                  {file.public_url && file.processing_status === 'completed' && (
                    <a
                      href={file.public_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-xs text-blue-600 hover:text-blue-800"
                    >
                      View
                    </a>
                  )}
                  <button
                    onClick={() => removeFile(file.id)}
                    className="text-gray-400 hover:text-red-600 transition-colors"
                    title="Remove file"
                  >
                    <XMarkIcon className="h-4 w-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Multi-Modal Processing Info */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-lg p-4">
        <h4 className="text-sm font-medium text-blue-900 mb-2">🎯 Multi-Modal Investment Analysis</h4>
        <ul className="text-xs text-blue-800 space-y-1">
          <li>• <strong>Pitch Decks (PDF/PPT):</strong> Business model, market analysis, financial projections</li>
          <li>• <strong>Audio Pitches:</strong> Presentation quality, message clarity, founder confidence</li>
          <li>• <strong>Video Presentations:</strong> Visual aids, speaker assessment, content delivery</li>
          <li>• <strong>Google Form Questionnaires:</strong> Structured founder responses and data collection</li>
          <li>• <strong>AI Integration:</strong> Synthesizes insights across all formats for comprehensive analysis</li>
          <li>• <strong>Investment Recommendation:</strong> INVEST/WATCH/PASS decision with confidence score</li>
        </ul>
        <div className="mt-2 p-2 bg-yellow-50 border border-yellow-200 rounded text-xs text-yellow-800">
          <strong>Investment Focus:</strong> AI analyzes all submission formats using standard VC evaluation frameworks. Google Form questionnaires provide structured founder input for enhanced analysis.
        </div>
      </div>
    </div>
  );
};

export default MultiModalUpload;