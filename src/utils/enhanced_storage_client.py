"""
Enhanced Google Cloud Storage client with file upload and processing capabilities
"""
import os
import time
import logging
from typing import Dict, Any, Optional, List
from google.cloud import storage
from google.api_core import exceptions
import mimetypes
import hashlib

logger = logging.getLogger(__name__)

class EnhancedStorageClient:
    """Enhanced Google Cloud Storage client with comprehensive file handling"""
    
    def __init__(self):
        """Initialize Google Cloud Storage client"""
        self.client = None
        self.bucket = None
        self.bucket_name = None
        self.initialized = False
        
        try:
            # Initialize Storage client
            self.client = storage.Client()
            
            # Set bucket name
            project_id = os.getenv('GOOGLE_CLOUD_PROJECT', 'startup-analyst-platform')
            self.bucket_name = f"{project_id}-files"
            
            # Get or create bucket
            self.bucket = self._get_or_create_bucket()
            
            if self.bucket:
                self.initialized = True
                logger.info(f"✅ Google Cloud Storage initialized - Bucket: {self.bucket_name}")
            else:
                logger.warning("⚠️ Failed to initialize storage bucket")
                
        except Exception as e:
            logger.warning(f"⚠️ Cloud Storage initialization failed: {str(e)}")
            logger.info("🔄 Continuing without Cloud Storage for development")
    
    def _get_or_create_bucket(self):
        """Get existing bucket or create new one"""
        try:
            # Try to get existing bucket
            bucket = self.client.bucket(self.bucket_name)
            bucket.reload()  # Check if bucket exists
            logger.info(f"✅ Using existing bucket: {self.bucket_name}")
            return bucket
            
        except exceptions.NotFound:
            # Create new bucket
            try:
                bucket = self.client.create_bucket(
                    self.bucket_name,
                    location="us-central1"
                )
                logger.info(f"✅ Created new bucket: {self.bucket_name}")
                return bucket
                
            except Exception as e:
                logger.error(f"❌ Failed to create bucket {self.bucket_name}: {str(e)}")
                logger.info("💡 You may need to choose a different bucket name or check permissions")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error accessing bucket {self.bucket_name}: {str(e)}")
            return None
    
    def upload_startup_file(self, file_data: bytes, filename: str, startup_id: str, 
                           content_type: Optional[str] = None) -> Dict[str, Any]:
        """Upload file for a specific startup"""
        if not self.initialized:
            raise Exception("Cloud Storage not initialized")
        
        try:
            # Generate safe filename with timestamp
            timestamp = int(time.time())
            safe_filename = self._sanitize_filename(filename)
            blob_name = f"startups/{startup_id}/{timestamp}_{safe_filename}"
            
            # Detect content type if not provided
            if not content_type:
                content_type, _ = mimetypes.guess_type(filename)
                if not content_type:
                    content_type = 'application/octet-stream'
            
            # Create blob and upload
            blob = self.bucket.blob(blob_name)
            blob.content_type = content_type
            
            # Upload file data
            blob.upload_from_string(file_data)
            
            # Make blob publicly readable
            blob.make_public()
            
            # Generate file hash for integrity
            file_hash = hashlib.md5(file_data).hexdigest()
            
            # Set metadata
            blob.metadata = {
                'startup_id': startup_id,
                'original_filename': filename,
                'upload_timestamp': str(timestamp),
                'file_hash': file_hash,
                'uploader': 'startup_analyst_platform'
            }
            blob.patch()
            
            result = {
                'success': True,
                'public_url': blob.public_url,
                'storage_path': blob_name,
                'bucket': self.bucket_name,
                'size': len(file_data),
                'content_type': content_type,
                'file_hash': file_hash,
                'timestamp': timestamp,
                'metadata': {
                    'startup_id': startup_id,
                    'original_filename': filename,
                    'size_mb': round(len(file_data) / (1024 * 1024), 2)
                }
            }
            
            logger.info(f"✅ File uploaded successfully: {filename} ({len(file_data)} bytes)")
            return result
            
        except Exception as e:
            logger.error(f"❌ File upload failed: {str(e)}")
            raise Exception(f"File upload failed: {str(e)}")
    
    def upload_demo_file(self, file_data: bytes, filename: str, 
                        file_type: str = "document") -> Dict[str, Any]:
        """Upload demo file for testing and demonstrations"""
        if not self.initialized:
            raise Exception("Cloud Storage not initialized")
        
        try:
            timestamp = int(time.time())
            safe_filename = self._sanitize_filename(filename)
            blob_name = f"demo/{file_type}/{timestamp}_{safe_filename}"
            
            # Detect content type
            content_type, _ = mimetypes.guess_type(filename)
            if not content_type:
                content_type = 'application/octet-stream'
            
            # Create and upload blob
            blob = self.bucket.blob(blob_name)
            blob.content_type = content_type
            blob.upload_from_string(file_data)
            blob.make_public()
            
            result = {
                'success': True,
                'public_url': blob.public_url,
                'storage_path': blob_name,
                'size': len(file_data),
                'content_type': content_type,
                'timestamp': timestamp,
                'file_type': file_type
            }
            
            logger.info(f"✅ Demo file uploaded: {filename}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Demo file upload failed: {str(e)}")
            raise Exception(f"Demo file upload failed: {str(e)}")
    
    def list_startup_files(self, startup_id: str) -> List[Dict[str, Any]]:
        """List all files for a specific startup"""
        if not self.initialized:
            return []
        
        try:
            prefix = f"startups/{startup_id}/"
            blobs = self.client.list_blobs(self.bucket_name, prefix=prefix)
            
            files = []
            for blob in blobs:
                file_info = {
                    'name': blob.name.split('/')[-1],  # Get filename without path
                    'storage_path': blob.name,
                    'public_url': blob.public_url,
                    'size': blob.size,
                    'content_type': blob.content_type,
                    'created': blob.time_created.isoformat() if blob.time_created else None,
                    'updated': blob.updated.isoformat() if blob.updated else None,
                    'metadata': blob.metadata or {}
                }
                files.append(file_info)
            
            logger.info(f"✅ Listed {len(files)} files for startup: {startup_id}")
            return files
            
        except Exception as e:
            logger.error(f"❌ Failed to list files for startup {startup_id}: {str(e)}")
            return []
    
    def delete_file(self, storage_path: str) -> bool:
        """Delete a file from storage"""
        if not self.initialized:
            return False
        
        try:
            blob = self.bucket.blob(storage_path)
            blob.delete()
            
            logger.info(f"✅ File deleted: {storage_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to delete file {storage_path}: {str(e)}")
            return False
    
    def get_file_info(self, storage_path: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a file"""
        if not self.initialized:
            return None
        
        try:
            blob = self.bucket.blob(storage_path)
            blob.reload()
            
            return {
                'name': blob.name.split('/')[-1],
                'storage_path': blob.name,
                'public_url': blob.public_url,
                'size': blob.size,
                'content_type': blob.content_type,
                'created': blob.time_created.isoformat() if blob.time_created else None,
                'updated': blob.updated.isoformat() if blob.updated else None,
                'metadata': blob.metadata or {},
                'etag': blob.etag,
                'generation': blob.generation
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to get file info for {storage_path}: {str(e)}")
            return None
    
    def generate_signed_url(self, storage_path: str, expiration_hours: int = 1) -> Optional[str]:
        """Generate signed URL for temporary access"""
        if not self.initialized:
            return None
        
        try:
            blob = self.bucket.blob(storage_path)
            
            # Generate signed URL valid for specified hours
            expiration = time.time() + (expiration_hours * 3600)
            
            url = blob.generate_signed_url(
                expiration=expiration,
                method='GET'
            )
            
            logger.info(f"✅ Generated signed URL for: {storage_path}")
            return url
            
        except Exception as e:
            logger.error(f"❌ Failed to generate signed URL for {storage_path}: {str(e)}")
            return None
    
    def extract_text_from_document(self, file_url: str) -> str:
        """Extract text from uploaded document (placeholder for future implementation)"""
        # TODO: Implement Google Document AI integration
        logger.info(f"📄 Text extraction not yet implemented for: {file_url}")
        return "Text extraction will be implemented with Google Document AI"
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """Get storage usage statistics"""
        if not self.initialized:
            return {"error": "Storage not initialized"}
        
        try:
            blobs = self.client.list_blobs(self.bucket_name)
            
            total_files = 0
            total_size = 0
            file_types = {}
            
            for blob in blobs:
                total_files += 1
                total_size += blob.size or 0
                
                # Count by content type
                content_type = blob.content_type or 'unknown'
                file_types[content_type] = file_types.get(content_type, 0) + 1
            
            return {
                'bucket_name': self.bucket_name,
                'total_files': total_files,
                'total_size_bytes': total_size,
                'total_size_mb': round(total_size / (1024 * 1024), 2),
                'file_types': file_types,
                'storage_url': f"gs://{self.bucket_name}"
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to get storage stats: {str(e)}")
            return {"error": str(e)}
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for safe storage"""
        # Remove path separators and other problematic characters
        safe_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-_"
        sanitized = "".join(c if c in safe_chars else "_" for c in filename)
        
        # Ensure it doesn't start with a dot or dash
        if sanitized.startswith(('.', '-')):
            sanitized = 'file_' + sanitized
        
        return sanitized[:100]  # Limit length
    
    def is_available(self) -> bool:
        """Check if storage is available and initialized"""
        return self.initialized

# Global instance
enhanced_storage_client = EnhancedStorageClient()
