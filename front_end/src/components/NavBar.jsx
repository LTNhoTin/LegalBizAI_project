import { useLocation, useNavigate, Link } from 'react-router-dom';
import { useState } from 'react';

function NavBar() {
  const navigate = useNavigate();
  const location = useLocation();
  const [hoveredTab, setHoveredTab] = useState(null);
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const customStyle = {
    color: 'hsl(22.47deg 93.52% 57.57%)',
    borderColor: 'hsl(22.47deg 93.52% 57.57%)',
  };

  const activeStyle = {
    ...customStyle,
    textDecoration: 'none',
    cursor: 'default',
  };

  const hoveredStyle = {
    color: 'white',
    borderColor: 'hsl(22.47deg 93.52% 57.57%)',
  };

  const getStyle = (path) => {
    if (location.pathname === path && hoveredTab === path) {
      return hoveredStyle;
    } else if (location.pathname === path) {
      return activeStyle;
    } else {
      return customStyle;
    }
  };

  const handleLinkClick = (path) => {
    setIsMenuOpen(false);
    navigate(path);
  };

  return (
    <div className="navbar bg-base-100 w-full max-w-screen-xl mx-auto px-4">
      <div className="navbar-start">
        <div className="dropdown">
          <label 
            tabIndex={0} 
            className="btn btn-ghost lg:hidden"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M4 6h16M4 12h8m-8 6h16"
              />
            </svg>
          </label>
          {isMenuOpen && (
            <ul
              tabIndex={0}
              className="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow bg-base-100 rounded-box w-52"
            >
              <li>
                <Link to="/" style={getStyle('/')} onClick={() => handleLinkClick('/')}>
                  Trang chủ
                </Link>
              </li>
              <li>
                <Link to="/chat" style={getStyle('/chat')} onClick={() => handleLinkClick('/chat')}>
                  Trò chuyện
                </Link>
              </li>
              <li>
                <Link to="/faq" style={getStyle('/faq')} onClick={() => handleLinkClick('/faq')}>
                  FAQs
                </Link>
              </li>
              <li>
                <Link to="/issue" style={getStyle('/issue')} onClick={() => handleLinkClick('/issue')}>
                  Báo lỗi/ Góp ý
                </Link>
              </li>
            </ul>
          )}
        </div>
        <a
          onClick={() => handleLinkClick("/")}
          className="btn btn-ghost normal-case font-extrabold text-xl bg-[linear-gradient(90deg,hsl(var(--s))_0%,hsl(var(--sf))_9%,hsl(var(--pf))_42%,hsl(var(--p))_47%,hsl(var(--a))_100%)] bg-clip-text will-change-auto [-webkit-text-fill-color:transparent] [transform:translate3d(0,0,0)] motion-reduce:!tracking-normal max-[1280px]:!tracking-normal [@supports(color:oklch(0_0_0))]:bg-[linear-gradient(90deg,hsl(var(--s))_4%,color-mix(in_oklch,hsl(var(--sf)),hsl(var(--pf)))_22%,hsl(var(--p))_45%,color-mix(in_oklch,hsl(var(--p)),hsl(var(--a)))_67%,hsl(var(--a))_100.2%)]"
        >
          FPTU LegalBot
        </a>
      </div>
      <div className="navbar-center hidden lg:flex">
        <ul className="menu menu-horizontal px-1 font-semibold">
          <li className="p-1">
            <button
              onClick={() => handleLinkClick("/")}
              style={getStyle('/')}
              className={location.pathname === "/" ? "btn btn-outline btn-primary" : ""}
              onMouseEnter={() => setHoveredTab('/')}
              onMouseLeave={() => setHoveredTab(null)}
            >
              Trang chủ
            </button>
          </li>
          <li className="p-1">
            <button
              onClick={() => handleLinkClick("/chat")}
              style={getStyle('/chat')}
              className={location.pathname === "/chat" ? "btn btn-outline btn-primary" : ""}
              onMouseEnter={() => setHoveredTab('/chat')}
              onMouseLeave={() => setHoveredTab(null)}
            >
              Trò chuyện
            </button>
          </li>
          <li className="p-1">
            <button
              onClick={() => handleLinkClick("/faq")}
              style={getStyle('/faq')}
              className={location.pathname === "/faq" ? "btn btn-outline btn-primary" : ""}
              onMouseEnter={() => setHoveredTab('/faq')}
              onMouseLeave={() => setHoveredTab(null)}
            >
              FAQs
            </button>
          </li>
          <li className="p-1">
            <button
              onClick={() => handleLinkClick("/issue")}
              style={getStyle('/issue')}
              className={location.pathname === "/issue" ? "btn btn-outline btn-primary" : ""}
              onMouseEnter={() => setHoveredTab('/issue')}
              onMouseLeave={() => setHoveredTab(null)}
            >
              Báo lỗi/ Góp ý
            </button>
          </li>
        </ul>
      </div>
      <div className="navbar-end">
        {/* <a className="btn btn-outline btn-primary md:flex hidden">
          Đăng nhập
        </a> */}
      </div>
    </div>
  );
}

export default NavBar;
