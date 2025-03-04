# Frontend Development Documentation

## Overview

The frontend for the Soccer Tournament Management System is built using React with TypeScript, focusing on a mobile-first design approach. The application serves different user roles including tournament organizers, referees, team managers, and fans.

## Technology Stack

- **Framework**: React with TypeScript
- **UI Components**: Material-UI (MUI)
- **State Management**: Redux Toolkit
- **Routing**: React Router
- **Forms**: Formik + Yup
- **API Client**: Axios
- **Build Tool**: Vite

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── layout/         # Layout components
│   ├── tournament/     # Tournament-related components
│   ├── match/          # Match-related components
│   └── shared/         # Shared/common components
├── features/           # Feature-specific components and logic
├── hooks/             # Custom React hooks
├── services/          # API services
├── store/             # Redux store configuration
├── types/             # TypeScript type definitions
└── utils/             # Utility functions
```

## User Scenarios

### 1. Tournament Organizer

#### Creating a New Tournament
1. Navigate to Tournaments section
2. Click "Create Tournament" button
3. Fill in tournament details:
   - Name
   - Start/End dates
   - Description
   - Tournament format (groups, knockout stages)
4. Create phases and groups
5. Set up match schedule template

#### Managing Teams
1. Add teams to tournament
2. Assign teams to groups
3. Review team rosters
4. Approve player registrations

#### Tournament Progress
1. Monitor ongoing matches
2. View standings and statistics
3. Manage phase transitions
4. Handle schedule changes

### 2. Team Manager

#### Team Registration
1. Register team for tournament
2. Add team details:
   - Team name
   - City
   - Team colors
   - Logo upload

#### Player Management
1. Add players to roster:
   - Player name
   - Number
   - Position
2. Update player information
3. View player statistics

#### Team Performance
1. View upcoming matches
2. Check team standings
3. Access team statistics
4. Review player performance

### 3. Referee

#### Match Management
1. Access assigned matches
2. Start match:
   - Confirm teams
   - Verify rosters
   - Record start time

#### Live Match Updates
1. Update score:
   - Record goals
   - Assign goal scorers
   - Track match time
2. End match:
   - Confirm final score
   - Submit match report

#### Match History
1. View previous matches
2. Access match reports
3. Review recorded events

### 4. Fan Experience

#### Tournament Overview
1. Browse active tournaments
2. View tournament brackets/groups
3. Check match schedules

#### Live Matches
1. View ongoing matches:
   - Live scores
   - Match statistics
   - Goal scorers
2. Receive real-time updates

#### Statistics and History
1. Access tournament statistics:
   - Top scorers
   - Team rankings
   - Match history
2. View team profiles
3. Check player statistics

## Development Phases

### Phase 1: Core Structure and Authentication
- [x] Project setup
- [x] Routing configuration
- [x] Layout components
- [ ] Authentication system
- [ ] User role management

### Phase 2: Tournament Management
- [ ] Tournament creation flow
- [ ] Team registration system
- [ ] Group/Phase management
- [ ] Schedule creation tools

### Phase 3: Match Management
- [ ] Match creation and scheduling
- [ ] Live match updates
- [ ] Score tracking
- [ ] Match statistics

### Phase 4: Statistics and Dashboards
- [ ] Team standings
- [ ] Player statistics
- [ ] Tournament analytics
- [ ] Performance dashboards

### Phase 5: Enhanced Features
- [ ] Real-time updates
- [ ] Advanced search
- [ ] Filters and sorting
- [ ] Export functionality

## MVP Iteration Cycles

### MVP 1: Core Tournament Viewing (Weeks 1-2)
**Focus**: Essential tournament viewing functionality for fans and organizers

#### Features
1. **Tournament List & Details**
   - Browse tournaments list
   - View tournament details
   - See groups and phases
   - Basic tournament search

2. **Team Information**
   - View team list
   - Basic team details
   - Team standings in groups

3. **Match Schedule**
   - View upcoming matches
   - Basic match details
   - Simple match list filtering

#### Success Criteria
- Users can browse tournaments without authentication
- Tournament information is clearly displayed
- Match schedule is easily accessible
- Mobile-responsive design works on all screens

### MVP 2: Tournament Management (Weeks 3-4)
**Focus**: Tournament creation and management for organizers

#### Features
1. **Tournament Creation**
   - Create new tournament wizard
   - Set up phases and groups
   - Configure tournament settings
   - Edit existing tournaments

2. **Team Management**
   - Add teams to tournament
   - Assign teams to groups
   - Basic team registration flow
   - Team roster management

3. **Schedule Management**
   - Create match schedule
   - Edit match details
   - Basic conflict detection
   - Schedule template support

#### Success Criteria
- Complete tournament setup in under 10 minutes
- Teams can be easily assigned to groups
- Match scheduling works efficiently
- All changes are saved and validated

### MVP 3: Match Management (Weeks 5-6)
**Focus**: Live match updates and scoring system

#### Features
1. **Match Operations**
   - Start/end matches
   - Live score updates
   - Goal recording
   - Basic match statistics

2. **Referee Interface**
   - Match control panel
   - Quick score updates
   - Goal attribution
   - Match report creation

3. **Real-time Updates**
   - Live score display
   - Basic notifications
   - Status updates
   - Simple live feed

#### Success Criteria
- Scores can be updated in under 5 seconds
- Match events are recorded accurately
- Real-time updates work reliably
- Interface is usable during live matches

### MVP 4: Statistics & Analytics (Weeks 7-8)
**Focus**: Comprehensive statistics and data visualization

#### Features
1. **Team Statistics**
   - Detailed performance metrics
   - Historical data
   - Comparative analysis
   - Visual representations

2. **Player Statistics**
   - Individual performance tracking
   - Goal statistics
   - Playing time tracking
   - Performance trends

3. **Tournament Analytics**
   - Group standings
   - Top performers
   - Tournament progress
   - Export capabilities

#### Success Criteria
- Statistics are accurate and up-to-date
- Data visualizations are clear and useful
- Performance metrics are easily understood
- Export functionality works correctly

### MVP 5: Enhanced Features (Weeks 9-10)
**Focus**: User experience improvements and advanced features

#### Features
1. **Advanced Search**
   - Full-text search
   - Filters and sorting
   - Search history
   - Saved searches

2. **Notifications**
   - Custom alerts
   - Match reminders
   - Score notifications
   - Important updates

3. **Social Features**
   - Share buttons
   - Tournament following
   - Basic comments
   - Favorite teams

#### Success Criteria
- Search results are fast and relevant
- Notifications are timely and useful
- Social features enhance engagement
- System performs well under load

## Development Workflow for Each MVP

### 1. Planning (2-3 days)
- Define detailed user stories
- Create component specifications
- Design API integration points
- Set up tracking metrics

### 2. Development (1 week)
- Implement core features
- Create/update components
- Write unit tests
- Integrate with API

### 3. Testing (2-3 days)
- Run automated tests
- Perform manual testing
- Cross-browser testing
- Mobile responsiveness checks

### 4. Review & Refinement (2-3 days)
- Code review
- Performance optimization
- Accessibility testing
- Documentation updates

### 5. Deployment & Monitoring (1-2 days)
- Staged deployment
- Monitor performance
- Gather user feedback
- Track usage metrics

## Key Metrics for Each MVP

### Performance Metrics
- Page load time < 2s
- Time to interactive < 3s
- API response time < 500ms
- Client-side rendering time < 100ms

### Quality Metrics
- Test coverage > 80%
- Zero critical bugs
- Accessibility score > 90
- Mobile usability score > 85

### User Experience Metrics
- Task completion rate > 90%
- Error rate < 5%
- User satisfaction score > 4/5
- Support ticket rate < 2%

## Component Examples

### Tournament Card
```tsx
<Card>
  <CardHeader
    title={tournament.name}
    subheader={`${format(tournament.startDate, 'PP')} - ${format(tournament.endDate, 'PP')}`}
  />
  <CardContent>
    <Typography>Teams: {tournament.teamsCount}</Typography>
    <Typography>Status: {tournament.status}</Typography>
  </CardContent>
  <CardActions>
    <Button>View Details</Button>
    <Button>Manage</Button>
  </CardActions>
</Card>
```

### Match Score Update
```tsx
<Paper elevation={3}>
  <Box p={2}>
    <Typography variant="h6">Update Score</Typography>
    <Grid container spacing={2} alignItems="center">
      <Grid item xs={5}>
        <Typography>{match.homeTeam}</Typography>
      </Grid>
      <Grid item xs={2}>
        <TextField
          type="number"
          value={homeScore}
          onChange={(e) => setHomeScore(Number(e.target.value))}
        />
      </Grid>
      <Grid item xs={5}>
        <Typography>{match.awayTeam}</Typography>
      </Grid>
    </Grid>
    <Button
      variant="contained"
      color="primary"
      onClick={handleScoreUpdate}
    >
      Update Score
    </Button>
  </Box>
</Paper>
```

## API Integration

### Tournament Service
```typescript
export const tournamentService = {
  getAll: () => axios.get('/api/tournaments'),
  getById: (id: number) => axios.get(`/api/tournaments/${id}`),
  create: (data: CreateTournamentDto) => axios.post('/api/tournaments', data),
  update: (id: number, data: UpdateTournamentDto) => 
    axios.put(`/api/tournaments/${id}`, data),
  delete: (id: number) => axios.delete(`/api/tournaments/${id}`)
};
```

## Error Handling

1. **API Errors**
```typescript
const handleApiError = (error: any) => {
  if (axios.isAxiosError(error)) {
    switch (error.response?.status) {
      case 401:
        // Handle unauthorized
        break;
      case 404:
        // Handle not found
        break;
      default:
        // Handle other errors
    }
  }
};
```

2. **Form Validation**
```typescript
const validationSchema = Yup.object({
  name: Yup.string().required('Tournament name is required'),
  startDate: Yup.date().required('Start date is required'),
  endDate: Yup.date()
    .min(Yup.ref('startDate'), 'End date must be after start date')
    .required('End date is required')
});
```

## Performance Considerations

1. **Data Fetching**
- Implement caching for tournament data
- Use pagination for large lists
- Optimize API calls with proper filtering

2. **Component Optimization**
- Lazy loading for routes
- Memoization of expensive calculations
- Virtual scrolling for long lists

3. **Asset Management**
- Optimize images
- Lazy load non-critical resources
- Implement proper caching strategies

## Accessibility

1. **Keyboard Navigation**
- Ensure all interactive elements are focusable
- Implement logical tab order
- Add keyboard shortcuts for common actions

2. **Screen Readers**
- Proper ARIA labels
- Semantic HTML structure
- Meaningful alt text for images

3. **Visual Accessibility**
- High contrast mode support
- Resizable text
- Color blind friendly design

## Testing Strategy

1. **Unit Tests**
- Component rendering
- State management
- Utility functions

2. **Integration Tests**
- User flows
- API integration
- Form submissions

3. **End-to-End Tests**
- Critical paths
- User scenarios
- Error handling

## Deployment

1. **Build Process**
```bash
# Production build
npm run build

# Preview build
npm run preview
```

2. **Environment Configuration**
```typescript
const API_URL = import.meta.env.VITE_API_URL;
const ENV = import.meta.env.VITE_ENV;
```

3. **Performance Monitoring**
- Implement error tracking
- Monitor page load times
- Track user interactions 