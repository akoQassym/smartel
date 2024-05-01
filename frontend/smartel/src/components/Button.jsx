import PropTypes from 'prop-types';

const Button = ({ onClick, className, bgColor, labelColor, children, ...props }) => {
  return (
    <button 
        onClick={onClick} 
        className={`px-4 py-2 rounded-md transition duration-300 ease-in-out shadow-sm hover:shadow-lg ${className}`}
        style={{
            backgroundColor: bgColor ?? '#34D399',
            color: labelColor ?? '#fff',
        }} 
        {...props}
    >
      {children}
    </button>
  )
}

Button.propTypes = {
  onClick: PropTypes.func.isRequired,
  className: PropTypes.string,
  bgColor: PropTypes.string,
  labelColor: PropTypes.string,
  children: PropTypes.node.isRequired,
};

export default Button;
