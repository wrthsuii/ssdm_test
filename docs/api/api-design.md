# API Design Documentation

## Architecture Overview
- **Base URL**: `http://localhost:3000/api/v1`
- **API Style**: RESTful
- **Authentication**: JWT Bearer tokens (planned)
- **Response Format**: JSON
- **Versioning Strategy**: URL path versioning (/v1, /v2)

## Resource Model
- Guest
- Account
- Room
- Booking
- Rating
- Notification

### User Resource
- **Endpoint**: `/guest`
- **Description**: A guest user in the system
- **Attributes**:
  - guestId (string): Unique identifier
  - email (string): User email
  - firstName (string): User first name
  - lastName (string): User last name
  - phone (string): User phone
- **Relationships**:
  - Has one booking

### Account Resource
- **Endpoint**: `/account`
- **Description**: System accounts management
- **Attributes**:
  - accountId (string): Unique identifier
  - email (string): User email
  - password (string): Account password
  - firstName (string): User first name
  - lastName (string): User last name
  - phone (string): User phone
  - role (enum): customer | staff | admin 
  - createdAt (datetime): Account creation datetime
- **Relationships**:
  - Has many bookings
  - Has many reviews

### Room Resource
- **Endpoint**: `/room`
- **Description**: Room management
- **Attributes**:
  - roomId (string): Unique identifier
  - roomType (enum): economy | standard | deluxe
  - maxGuest (integer): Max of guests in a room
  - basePrice (number): Price in UAH
  - roomStatus (enum): available | occupied | maintenance 
- **Relationships**:
  - Has many bookings 
  - Has many ratings
  - Has many amenities

## Design Decisions
==Examples, put your own here==

### Why Code-First?
We chose code-first approach because:
- Documentation stays synchronized with implementation
- Type safety through language features
- Faster development iterations
- No manual YAML maintenance

### Pagination Strategy
- Offset-based pagination for simplicity
- Default limit: 20 items
- Maximum limit: 100 items
- Returns metadata with total count and hasMore flag

### Error Handling
- Consistent error response structure
- Machine-readable error codes
- Human-friendly messages
- Validation errors include field details