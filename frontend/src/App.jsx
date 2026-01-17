import { useState, useEffect } from 'react'
import { Routes, Route } from 'react-router-dom'
import {
    Box,
    Container,
    Typography,
    Button,
    Card,
    CardContent,
    Grid,
    CircularProgress,
    Chip
} from '@mui/material'
import CloudUploadIcon from '@mui/icons-material/CloudUpload'
import WorkIcon from '@mui/icons-material/Work'
import SchoolIcon from '@mui/icons-material/School'
import TrendingUpIcon from '@mui/icons-material/TrendingUp'
import axios from 'axios'

// API Base URL
const API_BASE = 'http://localhost:8000'

function App() {
    const [healthStatus, setHealthStatus] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        // Check API health on mount
        axios.get(`${API_BASE}/health`)
            .then(res => {
                setHealthStatus(res.data)
                setLoading(false)
            })
            .catch(() => {
                setHealthStatus({ status: 'offline', message: 'Backend not running' })
                setLoading(false)
            })
    }, [])

    return (
        <Box sx={{ minHeight: '100vh' }}>
            {/* Hero Section */}
            <Box
                sx={{
                    pt: 12,
                    pb: 8,
                    textAlign: 'center',
                    position: 'relative',
                    overflow: 'hidden'
                }}
            >
                {/* Animated Background Orbs */}
                <Box
                    sx={{
                        position: 'absolute',
                        width: 400,
                        height: 400,
                        borderRadius: '50%',
                        background: 'radial-gradient(circle, rgba(99, 102, 241, 0.3) 0%, transparent 70%)',
                        top: -100,
                        left: -100,
                        animation: 'float 6s ease-in-out infinite',
                        zIndex: -1
                    }}
                />
                <Box
                    sx={{
                        position: 'absolute',
                        width: 300,
                        height: 300,
                        borderRadius: '50%',
                        background: 'radial-gradient(circle, rgba(244, 114, 182, 0.2) 0%, transparent 70%)',
                        bottom: -50,
                        right: -50,
                        animation: 'float 8s ease-in-out infinite reverse',
                        zIndex: -1
                    }}
                />

                <Container maxWidth="md">
                    {/* Logo & Title */}
                    <Typography
                        variant="h1"
                        sx={{
                            fontSize: { xs: '3rem', md: '4.5rem' },
                            fontWeight: 800,
                            mb: 2,
                            background: 'linear-gradient(135deg, #6366f1 0%, #f472b6 50%, #22d3ee 100%)',
                            backgroundClip: 'text',
                            WebkitBackgroundClip: 'text',
                            WebkitTextFillColor: 'transparent',
                            animation: 'gradient-shift 3s ease infinite',
                            backgroundSize: '200% 200%'
                        }}
                    >
                        Wevolve
                    </Typography>

                    <Typography
                        variant="h5"
                        sx={{
                            color: 'text.secondary',
                            mb: 4,
                            fontWeight: 300,
                            maxWidth: 600,
                            mx: 'auto'
                        }}
                    >
                        The AI-Powered Career Acceleration Ecosystem
                    </Typography>

                    {/* API Status Badge */}
                    <Chip
                        label={loading ? 'Connecting...' : healthStatus?.status === 'healthy' ? '🟢 Backend Connected' : '🔴 Backend Offline'}
                        variant="outlined"
                        sx={{
                            mb: 6,
                            borderColor: healthStatus?.status === 'healthy' ? 'success.main' : 'error.main',
                            color: healthStatus?.status === 'healthy' ? 'success.main' : 'error.main',
                        }}
                    />
                </Container>
            </Box>

            {/* Feature Cards */}
            <Container maxWidth="lg" sx={{ pb: 10 }}>
                <Grid container spacing={4}>
                    {/* Resume Intelligence */}
                    <Grid item xs={12} md={4}>
                        <Card
                            sx={{
                                height: '100%',
                                transition: 'all 0.3s ease',
                                '&:hover': {
                                    transform: 'translateY(-8px)',
                                    boxShadow: '0 20px 40px rgba(99, 102, 241, 0.3)',
                                }
                            }}
                        >
                            <CardContent sx={{ p: 4 }}>
                                <Box
                                    sx={{
                                        width: 64,
                                        height: 64,
                                        borderRadius: 3,
                                        background: 'linear-gradient(135deg, #6366f1 0%, #818cf8 100%)',
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'center',
                                        mb: 3,
                                        boxShadow: '0 8px 24px rgba(99, 102, 241, 0.4)'
                                    }}
                                >
                                    <CloudUploadIcon sx={{ fontSize: 32, color: 'white' }} />
                                </Box>
                                <Typography variant="h5" fontWeight={600} gutterBottom>
                                    Resume Intelligence
                                </Typography>
                                <Typography variant="body2" color="text.secondary" paragraph>
                                    Upload your resume and get instant AI-powered parsing with confidence scores.
                                    Know exactly how complete your profile is.
                                </Typography>
                                <Chip label="The Fix" size="small" color="primary" variant="outlined" />
                            </CardContent>
                        </Card>
                    </Grid>

                    {/* Transparent Matching */}
                    <Grid item xs={12} md={4}>
                        <Card
                            sx={{
                                height: '100%',
                                transition: 'all 0.3s ease',
                                '&:hover': {
                                    transform: 'translateY(-8px)',
                                    boxShadow: '0 20px 40px rgba(244, 114, 182, 0.3)',
                                }
                            }}
                        >
                            <CardContent sx={{ p: 4 }}>
                                <Box
                                    sx={{
                                        width: 64,
                                        height: 64,
                                        borderRadius: 3,
                                        background: 'linear-gradient(135deg, #f472b6 0%, #f9a8d4 100%)',
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'center',
                                        mb: 3,
                                        boxShadow: '0 8px 24px rgba(244, 114, 182, 0.4)'
                                    }}
                                >
                                    <WorkIcon sx={{ fontSize: 32, color: 'white' }} />
                                </Box>
                                <Typography variant="h5" fontWeight={600} gutterBottom>
                                    Transparent Matching
                                </Typography>
                                <Typography variant="body2" color="text.secondary" paragraph>
                                    See exactly why you match with a job. Our multi-factor engine explains
                                    every score: Skills (40%), Location, Salary, and more.
                                </Typography>
                                <Chip label="The Why" size="small" color="secondary" variant="outlined" />
                            </CardContent>
                        </Card>
                    </Grid>

                    {/* Actionable Growth */}
                    <Grid item xs={12} md={4}>
                        <Card
                            sx={{
                                height: '100%',
                                transition: 'all 0.3s ease',
                                '&:hover': {
                                    transform: 'translateY(-8px)',
                                    boxShadow: '0 20px 40px rgba(34, 211, 238, 0.3)',
                                }
                            }}
                        >
                            <CardContent sx={{ p: 4 }}>
                                <Box
                                    sx={{
                                        width: 64,
                                        height: 64,
                                        borderRadius: 3,
                                        background: 'linear-gradient(135deg, #22d3ee 0%, #67e8f9 100%)',
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'center',
                                        mb: 3,
                                        boxShadow: '0 8px 24px rgba(34, 211, 238, 0.4)'
                                    }}
                                >
                                    <SchoolIcon sx={{ fontSize: 32, color: 'white' }} />
                                </Box>
                                <Typography variant="h5" fontWeight={600} gutterBottom>
                                    Actionable Growth
                                </Typography>
                                <Typography variant="body2" color="text.secondary" paragraph>
                                    Get a personalized learning roadmap based on your skill gaps.
                                    We show you how to become the perfect candidate.
                                </Typography>
                                <Chip label="The How" size="small" sx={{ borderColor: '#22d3ee', color: '#22d3ee' }} variant="outlined" />
                            </CardContent>
                        </Card>
                    </Grid>
                </Grid>

                {/* CTA Button */}
                <Box sx={{ textAlign: 'center', mt: 8 }}>
                    <Button
                        variant="contained"
                        size="large"
                        startIcon={<TrendingUpIcon />}
                        sx={{
                            px: 6,
                            py: 2,
                            fontSize: '1.1rem',
                            background: 'linear-gradient(135deg, #6366f1 0%, #f472b6 100%)',
                            boxShadow: '0 8px 24px rgba(99, 102, 241, 0.4)',
                            '&:hover': {
                                transform: 'scale(1.05)',
                                boxShadow: '0 12px 32px rgba(99, 102, 241, 0.5)',
                            },
                            transition: 'all 0.3s ease'
                        }}
                    >
                        Start Your Evolution
                    </Button>
                    <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
                        Upload your resume to get started →
                    </Typography>
                </Box>
            </Container>

            {/* Footer */}
            <Box
                sx={{
                    py: 4,
                    textAlign: 'center',
                    borderTop: '1px solid rgba(255,255,255,0.1)',
                    mt: 'auto'
                }}
            >
                <Typography variant="body2" color="text.secondary">
                    Built with ❤️ by <strong>Kasukabe Defence Group</strong>
                </Typography>
            </Box>
        </Box>
    )
}

export default App
