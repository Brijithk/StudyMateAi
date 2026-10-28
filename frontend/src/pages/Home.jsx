import { Link } from "react-router-dom";

function Home() {
  return (
    <main className="home">
      <nav className="navbar">
        <Link to="/" className="brand">
          StudyMate AI
        </Link>

        <div className="nav-links">
          <Link to="/login" className="nav-link">
            Login
          </Link>

          <Link to="/register" className="btn btn-primary">
            Get Started
          </Link>
        </div>
      </nav>

      <section className="hero">
        <span className="hero-badge">Your AI-powered study companion</span>

        <h1>
          Learn Smarter.
          <br />
          <span>Study Better.</span>
        </h1>

        <p>
          Upload your study materials, ask questions about your notes,
          and prepare for exams with your personal AI study assistant.
        </p>

        <div className="hero-actions">
          <Link to="/register" className="btn btn-primary">
            Get Started Free
          </Link>

          <Link to="/login" className="btn btn-secondary">
            Sign In
          </Link>
        </div>

        <div className="features">
          <article className="feature-card">
            <div className="feature-icon">📚</div>
            <h2>Document Learning</h2>
            <p>Upload PDFs and keep your study materials organized.</p>
          </article>

          <article className="feature-card">
            <div className="feature-icon">🤖</div>
            <h2>AI Document Chat</h2>
            <p>Ask questions and get answers grounded in your notes.</p>
          </article>

          <article className="feature-card">
            <div className="feature-icon">🎯</div>
            <h2>Exam Preparation</h2>
            <p>Build a foundation for summaries, quizzes, and revision.</p>
          </article>
        </div>
      </section>

      <footer className="footer">
        StudyMate AI — Your learning journey, made smarter.
      </footer>
    </main>
  );
}

export default Home;