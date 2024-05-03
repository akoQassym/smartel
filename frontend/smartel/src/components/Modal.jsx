import { useEffect } from 'react';
import PropTypes from 'prop-types';

const Modal = ({ isOpen, onClose, children }) => {
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'auto';
    }
    return () => {
      document.body.style.overflow = 'auto';
    };
  }, [isOpen]);

  return (
    <div className={`fixed inset-0 ${isOpen ? '' : 'hidden'}`}>
      <div className="flex items-center justify-center h-full">
        <div className="fixed inset-0 bg-black opacity-50"></div>
        <div className="relative bg-white rounded-lg w-1/2 z-100">
          <div className="absolute top-0 right-0 p-2">
            <button className="text-gray-500 hover:text-gray-800" onClick={onClose}>
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
          <div className="p-6">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Modal;

Modal.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  children: PropTypes.node.isRequired,
};
