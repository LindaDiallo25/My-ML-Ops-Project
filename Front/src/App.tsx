import { useState, useRef } from 'react';
import { Upload, Sparkles, Loader2, Check } from 'lucide-react';
import { Button } from './components/ui/button';
import { Card } from './components/ui/card';
import { motion, AnimatePresence } from 'motion/react';
import { ImageWithFallback } from './components/figma/ImageWithFallback';

type ClassificationResult = {
  label: 'dandelion' | 'grass';
  confidence: number;
};

export default function App() {
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [isClassifying, setIsClassifying] = useState(false);
  const [result, setResult] = useState<ClassificationResult | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (file: File) => {
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setSelectedImage(e.target?.result as string);
        setResult(null);
        // Simulate classification (you'll replace this with actual API call)
        simulateClassification();
      };
      reader.readAsDataURL(file);
    }
  };

  const simulateClassification = () => {
    setIsClassifying(true);
    // Simulate API call - replace this with your actual classification logic
    setTimeout(() => {
      const mockResult: ClassificationResult = {
        label: Math.random() > 0.5 ? 'dandelion' : 'grass',
        confidence: Math.random() * 30 + 70, // 70-100%
      };
      setResult(mockResult);
      setIsClassifying(false);
    }, 2000);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  const handleReset = () => {
    setSelectedImage(null);
    setResult(null);
    setIsClassifying(false);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-green-50 to-yellow-50">
      {/* Background Pattern */}
      <div className="fixed inset-0 opacity-[0.03] pointer-events-none">
        <div className="absolute inset-0" style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23000000' fill-opacity='1'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
        }} />
      </div>

      <div className="relative z-10 container mx-auto px-4 py-12 max-w-4xl">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-green-400 to-emerald-500 rounded-full mb-6 shadow-lg">
            <Sparkles className="w-10 h-10 text-white" />
          </div>
          <h1 className="mb-4 bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
            Dandelion vs Grass Classifier
          </h1>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Upload an image and let the model identify whether it's a dandelion or grass. 
          </p>
        </motion.div>

        {/* Main Content */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <Card className="p-8 shadow-2xl border-0 bg-white/80 backdrop-blur-sm">
            {!selectedImage ? (
              /* Upload Area */
              <div
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                className={`border-2 border-dashed rounded-xl p-12 text-center transition-all duration-300 cursor-pointer ${
                  isDragging
                    ? 'border-green-500 bg-green-50 scale-[1.02]'
                    : 'border-gray-300 hover:border-green-400 hover:bg-gray-50'
                }`}
                onClick={() => fileInputRef.current?.click()}
              >
                <div className="flex flex-col items-center gap-4">
                  <div className={`w-24 h-24 rounded-full flex items-center justify-center transition-all duration-300 ${
                    isDragging ? 'bg-green-100 scale-110' : 'bg-gray-100'
                  }`}>
                    <Upload className={`w-12 h-12 transition-colors duration-300 ${
                      isDragging ? 'text-green-500' : 'text-gray-400'
                    }`} />
                  </div>
                  <div>
                    <p className="mb-2 text-gray-700">
                      <span className="text-green-600">Click to upload</span> or drag and drop
                    </p>
                    <p className="text-gray-500">PNG, JPG, GIF up to 10MB</p>
                  </div>
                </div>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  onChange={handleFileInputChange}
                  className="hidden"
                />
              </div>
            ) : (
              /* Image Preview & Results */
              <div className="space-y-6">
                {/* Image Display */}
                <motion.div
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="relative rounded-xl overflow-hidden bg-gray-100 shadow-lg"
                >
                  <ImageWithFallback
                    src={selectedImage}
                    alt="Uploaded image"
                    className="w-full h-auto max-h-96 object-contain"
                  />
                </motion.div>

                {/* Classification Status */}
                <AnimatePresence mode="wait">
                  {isClassifying ? (
                    <motion.div
                      key="classifying"
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -20 }}
                      className="flex items-center justify-center gap-3 p-6 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl"
                    >
                      <Loader2 className="w-6 h-6 animate-spin text-blue-500" />
                      <span className="text-gray-700">Classifying your image...</span>
                    </motion.div>
                  ) : result ? (
                    <motion.div
                      key="result"
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -20 }}
                      className={`p-6 rounded-xl ${
                        result.label === 'dandelion'
                          ? 'bg-gradient-to-r from-yellow-50 to-amber-50'
                          : 'bg-gradient-to-r from-green-50 to-emerald-50'
                      }`}
                    >
                      <div className="flex items-start gap-4">
                        <div className={`w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0 ${
                          result.label === 'dandelion'
                            ? 'bg-yellow-100'
                            : 'bg-green-100'
                        }`}>
                          {result.label === 'dandelion' ? (
                            <span className="text-2xl">🌼</span>
                          ) : (
                            <span className="text-2xl">🌱</span>
                          )}
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-2">
                            <Check className={`w-5 h-5 ${
                              result.label === 'dandelion' ? 'text-yellow-600' : 'text-green-600'
                            }`} />
                            <span className="text-gray-900">
                              Classification Complete
                            </span>
                          </div>
                          <p className="text-gray-700 mb-3">
                            This image is classified as:{' '}
                            <span className={`capitalize ${
                              result.label === 'dandelion' ? 'text-yellow-700' : 'text-green-700'
                            }`}>
                              {result.label}
                            </span>
                          </p>
                          <div className="space-y-2">
                            <div className="flex items-center justify-between text-gray-600">
                              <span>Confidence</span>
                              <span>{result.confidence.toFixed(1)}%</span>
                            </div>
                            <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                              <motion.div
                                initial={{ width: 0 }}
                                animate={{ width: `${result.confidence}%` }}
                                transition={{ duration: 1, ease: "easeOut" }}
                                className={`h-full ${
                                  result.label === 'dandelion'
                                    ? 'bg-gradient-to-r from-yellow-400 to-amber-500'
                                    : 'bg-gradient-to-r from-green-400 to-emerald-500'
                                }`}
                              />
                            </div>
                          </div>
                        </div>
                      </div>
                    </motion.div>
                  ) : null}
                </AnimatePresence>

                {/* Action Buttons */}
                <div className="flex gap-3">
                  <Button
                    onClick={handleReset}
                    variant="outline"
                    className="flex-1"
                  >
                    <Upload className="w-4 h-4 mr-2" />
                    Upload Another
                  </Button>
                  {result && (
                    <Button
                      onClick={simulateClassification}
                      className="flex-1 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700"
                    >
                      <Sparkles className="w-4 h-4 mr-2" />
                      Reclassify
                    </Button>
                  )}
                </div>
              </div>
            )}
          </Card>
        </motion.div>

        {/* Info Cards */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="grid md:grid-cols-2 gap-6 mt-8"
        >
          <Card className="p-6 bg-white/60 backdrop-blur-sm border-0 shadow-lg">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center flex-shrink-0">
                <span className="text-2xl">🌼</span>
              </div>
              <div>
                <h3 className="mb-2 text-gray-900">Dandelions</h3>
                <p className="text-gray-600">
                  Bright yellow flowers with distinctive jagged leaves and fluffy seed heads.
                </p>
              </div>
            </div>
          </Card>

          <Card className="p-6 bg-white/60 backdrop-blur-sm border-0 shadow-lg">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center flex-shrink-0">
                <span className="text-2xl">🌱</span>
              </div>
              <div>
                <h3 className="mb-2 text-gray-900">Grass</h3>
                <p className="text-gray-600">
                  Long, narrow blades forming dense green lawns and meadows.
                </p>
              </div>
            </div>
          </Card>
        </motion.div>
      </div>
    </div>
  );
}
