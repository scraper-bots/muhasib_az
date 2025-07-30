# BirJob Android Development Guide

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture & Technology Stack](#architecture--technology-stack)
3. [Project Structure](#project-structure)
4. [Core Features Implementation](#core-features-implementation)
5. [Backend Integration](#backend-integration)
6. [UI/UX Implementation](#uiux-implementation)
7. [Push Notifications](#push-notifications)
8. [Data Models](#data-models)
9. [Services & Managers](#services--managers)
10. [Views & Screens](#views--screens)
11. [Navigation Flow](#navigation-flow)
12. [Testing Strategy](#testing-strategy)
13. [Performance Optimization](#performance-optimization)
14. [Deployment Guide](#deployment-guide)

---

## Project Overview

**App Name**: BirJob (Android Version)  
**Platform**: Android (Kotlin/Java)  
**Purpose**: Job matching and notification system with AI-powered job recommendations  
**Target Android Version**: API 24+ (Android 7.0+) for broad compatibility  
**Architecture**: MVVM with Repository Pattern  

### Key Features
- Real-time job matching with push notifications
- AI-powered job recommendations and chat
- Analytics dashboard with market insights
- Notification inbox with smart filtering
- Direct job application integration
- Keyword-based job alerts
- Privacy-focused data handling

---

## Architecture & Technology Stack

### **Technology Stack**
```
Frontend: Kotlin + Jetpack Compose
Architecture: MVVM + Repository Pattern
DI: Hilt (Dagger)
Networking: Retrofit + OkHttp
Database: Room + SQLite
Push Notifications: Firebase Cloud Messaging (FCM)
Image Loading: Coil
Async: Coroutines + Flow
Navigation: Jetpack Navigation Compose
Testing: JUnit + Espresso + Compose Testing
```

### **Project Dependencies (build.gradle)**
```kotlin
dependencies {
    // Core Android
    implementation 'androidx.core:core-ktx:1.12.0'
    implementation 'androidx.lifecycle:lifecycle-runtime-ktx:2.7.0'
    implementation 'androidx.activity:activity-compose:1.8.2'
    
    // Compose BOM
    implementation platform('androidx.compose:compose-bom:2024.02.00')
    implementation 'androidx.compose.ui:ui'
    implementation 'androidx.compose.ui:ui-graphics'
    implementation 'androidx.compose.ui:ui-tooling-preview'
    implementation 'androidx.compose.material3:material3'
    
    // Navigation
    implementation 'androidx.navigation:navigation-compose:2.7.6'
    
    // ViewModel
    implementation 'androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0'
    
    // Hilt
    implementation 'com.google.dagger:hilt-android:2.48'
    kapt 'com.google.dagger:hilt-compiler:2.48'
    implementation 'androidx.hilt:hilt-navigation-compose:1.1.0'
    
    // Networking
    implementation 'com.squareup.retrofit2:retrofit:2.9.0'
    implementation 'com.squareup.retrofit2:converter-gson:2.9.0'
    implementation 'com.squareup.okhttp3:logging-interceptor:4.12.0'
    
    // Room Database
    implementation 'androidx.room:room-runtime:2.6.1'
    implementation 'androidx.room:room-ktx:2.6.1'
    kapt 'androidx.room:room-compiler:2.6.1'
    
    // Firebase
    implementation 'com.google.firebase:firebase-messaging:23.4.0'
    implementation 'com.google.firebase:firebase-analytics:21.5.0'
    
    // Image Loading
    implementation 'io.coil-kt:coil-compose:2.5.0'
    
    // Charts for Analytics
    implementation 'com.github.PhilJay:MPAndroidChart:v3.1.0'
    
    // WebView
    implementation 'androidx.webkit:webkit:1.9.0'
    
    // Testing
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
    androidTestImplementation 'androidx.compose.ui:ui-test-junit4'
    debugImplementation 'androidx.compose.ui:ui-tooling'
    debugImplementation 'androidx.compose.ui:ui-test-manifest'
}
```

---

## Project Structure

```
app/
├── src/
│   ├── main/
│   │   ├── java/com/birjob/android/
│   │   │   ├── di/                     # Dependency Injection
│   │   │   │   ├── NetworkModule.kt
│   │   │   │   ├── DatabaseModule.kt
│   │   │   │   └── AppModule.kt
│   │   │   ├── data/                   # Data Layer
│   │   │   │   ├── local/              # Room Database
│   │   │   │   │   ├── dao/
│   │   │   │   │   ├── entities/
│   │   │   │   │   └── database/
│   │   │   │   ├── remote/             # API Services
│   │   │   │   │   ├── api/
│   │   │   │   │   ├── dto/
│   │   │   │   │   └── interceptors/
│   │   │   │   └── repository/         # Repository Pattern
│   │   │   ├── domain/                 # Domain Layer
│   │   │   │   ├── model/              # Domain Models
│   │   │   │   ├── repository/         # Repository Interfaces
│   │   │   │   └── usecase/            # Use Cases
│   │   │   ├── presentation/           # UI Layer
│   │   │   │   ├── ui/
│   │   │   │   │   ├── screens/        # Compose Screens
│   │   │   │   │   ├── components/     # Reusable Components
│   │   │   │   │   ├── theme/          # App Theme
│   │   │   │   │   └── navigation/     # Navigation
│   │   │   │   ├── viewmodel/          # ViewModels
│   │   │   │   └── state/              # UI State Classes
│   │   │   ├── service/                # Background Services
│   │   │   │   ├── NotificationService.kt
│   │   │   │   └── JobSyncService.kt
│   │   │   └── util/                   # Utilities
│   │   │       ├── Constants.kt
│   │   │       ├── Extensions.kt
│   │   │       └── NetworkUtils.kt
│   │   ├── res/                        # Resources
│   │   └── AndroidManifest.xml
│   ├── test/                           # Unit Tests
│   └── androidTest/                    # Integration Tests
└── build.gradle
```

---

## Core Features Implementation

### **1. Job Search & Matching**

#### JobSearchViewModel.kt
```kotlin
@HiltViewModel
class JobSearchViewModel @Inject constructor(
    private val jobRepository: JobRepository,
    private val analyticsRepository: AnalyticsRepository
) : ViewModel() {
    
    private val _jobs = MutableStateFlow<List<Job>>(emptyList())
    val jobs: StateFlow<List<Job>> = _jobs.asStateFlow()
    
    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()
    
    private val _searchQuery = MutableStateFlow("")
    val searchQuery: StateFlow<String> = _searchQuery.asStateFlow()
    
    fun searchJobs(query: String, location: String? = null) {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val searchResult = jobRepository.searchJobs(
                    query = query,
                    location = location,
                    limit = 50
                )
                _jobs.value = searchResult.jobs
                
                // Track search analytics
                analyticsRepository.trackSearchEvent(query, searchResult.jobs.size)
            } catch (e: Exception) {
                // Handle error
            } finally {
                _isLoading.value = false
            }
        }
    }
    
    fun saveJob(job: Job) {
        viewModelScope.launch {
            jobRepository.saveJob(job)
        }
    }
    
    fun applyToJob(job: Job) {
        viewModelScope.launch {
            // Track application
            analyticsRepository.trackJobApplication(job.id, job.source)
            
            // Open external application URL
            // Will be handled by UI layer
        }
    }
}
```

#### JobSearchScreen.kt
```kotlin
@Composable
fun JobSearchScreen(
    viewModel: JobSearchViewModel = hiltViewModel(),
    onJobClick: (Job) -> Unit,
    onApplyClick: (Job) -> Unit
) {
    val jobs by viewModel.jobs.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()
    val searchQuery by viewModel.searchQuery.collectAsState()
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        // Search Bar
        SearchBar(
            query = searchQuery,
            onQueryChange = viewModel::updateSearchQuery,
            onSearch = { viewModel.searchJobs(it) },
            modifier = Modifier.fillMaxWidth()
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        // Job Results
        when {
            isLoading -> {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    CircularProgressIndicator()
                }
            }
            jobs.isEmpty() -> {
                EmptyJobsState()
            }
            else -> {
                LazyColumn {
                    items(jobs) { job ->
                        JobCard(
                            job = job,
                            onJobClick = { onJobClick(job) },
                            onApplyClick = { onApplyClick(job) },
                            onSaveClick = { viewModel.saveJob(job) }
                        )
                    }
                }
            }
        }
    }
}
```

### **2. Notification System**

#### NotificationService.kt
```kotlin
@AndroidEntryPoint
class BirJobFirebaseMessagingService : FirebaseMessagingService() {
    
    @Inject
    lateinit var notificationRepository: NotificationRepository
    
    @Inject
    lateinit var jobRepository: JobRepository
    
    override fun onMessageReceived(remoteMessage: RemoteMessage) {
        super.onMessageReceived(remoteMessage)
        
        Log.d("FCM", "Message received: ${remoteMessage.data}")
        
        // Parse notification data
        val notificationData = parseNotificationData(remoteMessage.data)
        
        when (notificationData.type) {
            NotificationType.JOB_MATCH -> handleJobMatchNotification(notificationData)
            NotificationType.BULK_JOB_MATCH -> handleBulkJobMatchNotification(notificationData)
            NotificationType.JOB_ALERT -> handleJobAlertNotification(notificationData)
            NotificationType.SYSTEM -> handleSystemNotification(notificationData)
        }
    }
    
    private fun handleJobMatchNotification(data: NotificationData) {
        // Save to local database
        runBlocking {
            notificationRepository.saveNotification(data)
        }
        
        // Show system notification
        showSystemNotification(
            title = data.title,
            body = data.message,
            data = data
        )
    }
    
    private fun showSystemNotification(
        title: String,
        body: String,
        data: NotificationData
    ) {
        val intent = Intent(this, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
            putExtra("notification_id", data.id)
            putExtra("notification_type", data.type.name)
        }
        
        val pendingIntent = PendingIntent.getActivity(
            this, 0, intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
        
        val notification = NotificationCompat.Builder(this, CHANNEL_ID)
            .setSmallIcon(R.drawable.ic_notification)
            .setContentTitle(title)
            .setContentText(body)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setContentIntent(pendingIntent)
            .setAutoCancel(true)
            .addAction(
                R.drawable.ic_visibility,
                "View Jobs",
                pendingIntent
            )
            .build()
        
        NotificationManagerCompat.from(this).notify(data.id.hashCode(), notification)
    }
    
    override fun onNewToken(token: String) {
        super.onNewToken(token)
        Log.d("FCM", "New token: $token")
        
        // Send token to server
        runBlocking {
            try {
                notificationRepository.registerDeviceToken(token)
            } catch (e: Exception) {
                Log.e("FCM", "Failed to register token", e)
            }
        }
    }
    
    companion object {
        const val CHANNEL_ID = "birjob_notifications"
    }
}
```

### **3. Analytics Dashboard**

#### AnalyticsViewModel.kt
```kotlin
@HiltViewModel
class AnalyticsViewModel @Inject constructor(
    private val analyticsRepository: AnalyticsRepository
) : ViewModel() {
    
    private val _marketOverview = MutableStateFlow<MarketOverview?>(null)
    val marketOverview: StateFlow<MarketOverview?> = _marketOverview.asStateFlow()
    
    private val _keywordTrends = MutableStateFlow<List<KeywordTrend>>(emptyList())
    val keywordTrends: StateFlow<List<KeywordTrend>> = _keywordTrends.asStateFlow()
    
    private val _companyAnalytics = MutableStateFlow<List<CompanyAnalytic>>(emptyList())
    val companyAnalytics: StateFlow<List<CompanyAnalytic>> = _companyAnalytics.asStateFlow()
    
    private val _remoteWorkAnalysis = MutableStateFlow<RemoteWorkAnalysis?>(null)
    val remoteWorkAnalysis: StateFlow<RemoteWorkAnalysis?> = _remoteWorkAnalysis.asStateFlow()
    
    init {
        loadAnalyticsData()
    }
    
    private fun loadAnalyticsData() {
        viewModelScope.launch {
            try {
                // Load all analytics data in parallel
                val marketOverviewDeferred = async { analyticsRepository.getMarketOverview() }
                val keywordTrendsDeferred = async { analyticsRepository.getKeywordTrends() }
                val companyAnalyticsDeferred = async { analyticsRepository.getCompanyAnalytics() }
                val remoteWorkDeferred = async { analyticsRepository.getRemoteWorkAnalysis() }
                
                _marketOverview.value = marketOverviewDeferred.await()
                _keywordTrends.value = keywordTrendsDeferred.await()
                _companyAnalytics.value = companyAnalyticsDeferred.await()
                _remoteWorkAnalysis.value = remoteWorkDeferred.await()
                
            } catch (e: Exception) {
                // Handle error
                Log.e("Analytics", "Failed to load analytics data", e)
            }
        }
    }
    
    fun refreshData() {
        loadAnalyticsData()
    }
}
```

#### AnalyticsScreen.kt
```kotlin
@Composable
fun AnalyticsScreen(
    viewModel: AnalyticsViewModel = hiltViewModel()
) {
    val marketOverview by viewModel.marketOverview.collectAsState()
    val keywordTrends by viewModel.keywordTrends.collectAsState()
    val companyAnalytics by viewModel.companyAnalytics.collectAsState()
    val remoteWorkAnalysis by viewModel.remoteWorkAnalysis.collectAsState()
    
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        // Market Overview Card
        item {
            marketOverview?.let { overview ->
                MarketOverviewCard(overview = overview)
            }
        }
        
        // Keyword Trends Chart
        item {
            KeywordTrendsChart(trends = keywordTrends)
        }
        
        // Company Analytics
        item {
            CompanyAnalyticsSection(analytics = companyAnalytics)
        }
        
        // Remote Work Analysis
        item {
            remoteWorkAnalysis?.let { analysis ->
                RemoteWorkAnalysisCard(analysis = analysis)
            }
        }
    }
}

@Composable
fun MarketOverviewCard(overview: MarketOverview) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        elevation = CardDefaults.cardElevation(defaultElevation = 4.dp)
    ) {
        Column(
            modifier = Modifier.padding(16.dp)
        ) {
            Text(
                text = "Market Overview",
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.Bold
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                StatisticItem(
                    label = "Total Jobs",
                    value = overview.totalJobs.toString(),
                    icon = Icons.Default.Work
                )
                
                StatisticItem(
                    label = "New Today",
                    value = overview.newJobsToday.toString(),
                    icon = Icons.Default.TrendingUp
                )
                
                StatisticItem(
                    label = "Companies",
                    value = overview.totalCompanies.toString(),
                    icon = Icons.Default.Business
                )
            }
        }
    }
}
```

---

## Backend Integration

### **API Service Layer**

#### ApiService.kt
```kotlin
interface ApiService {
    
    // Job Search
    @GET("api/v1/jobs/")
    suspend fun searchJobs(
        @Query("query") query: String?,
        @Query("location") location: String?,
        @Query("limit") limit: Int = 20,
        @Query("offset") offset: Int = 0
    ): JobSearchResponse
    
    @GET("api/v1/jobs/{jobId}")
    suspend fun getJobById(@Path("jobId") jobId: Int): JobDetailResponse
    
    // Saved Jobs
    @POST("api/v1/jobs/save")
    suspend fun saveJob(@Body request: SaveJobRequest): SaveJobResponse
    
    @GET("api/v1/jobs/saved")
    suspend fun getSavedJobs(): SavedJobsResponse
    
    @DELETE("api/v1/jobs/saved/{jobId}")
    suspend fun removeSavedJob(@Path("jobId") jobId: Int): BaseResponse
    
    // Notifications
    @GET("api/v1/notifications/inbox/{deviceId}")
    suspend fun getNotificationInbox(
        @Path("deviceId") deviceId: String,
        @Query("limit") limit: Int = 50,
        @Query("offset") offset: Int = 0
    ): NotificationInboxResponse
    
    @POST("api/v1/notifications/mark-read/{notificationId}")
    suspend fun markNotificationAsRead(
        @Path("notificationId") notificationId: String
    ): MarkAsReadResponse
    
    @POST("api/v1/notifications/mark-all-read")
    suspend fun markAllNotificationsAsRead(): MarkAsReadResponse
    
    @DELETE("api/v1/notifications/{notificationId}")
    suspend fun deleteNotification(
        @Path("notificationId") notificationId: String
    ): DeleteNotificationResponse
    
    // Device Registration
    @POST("api/v1/device/register")
    suspend fun registerDevice(@Body request: DeviceRegistrationRequest): DeviceRegistrationResponse
    
    @POST("api/v1/device/push-token")
    suspend fun registerPushToken(@Body request: PushTokenRequest): PushTokenResponse
    
    // Analytics
    @GET("api/v1/analytics/market-overview")
    suspend fun getMarketOverview(): MarketOverviewResponse
    
    @GET("api/v1/analytics/keyword-trends")
    suspend fun getKeywordTrends(): KeywordTrendsResponse
    
    @GET("api/v1/analytics/company-analytics")
    suspend fun getCompanyAnalytics(@Query("limit") limit: Int = 20): CompanyAnalyticsResponse
    
    @GET("api/v1/analytics/remote-work-analysis")
    suspend fun getRemoteWorkAnalysis(): RemoteWorkAnalysisResponse
    
    // AI Chat
    @POST("api/v1/chat/send")
    suspend fun sendChatMessage(@Body request: ChatRequest): ChatResponse
    
    // Event Tracking
    @POST("api/v1/analytics/track")
    suspend fun trackEvent(@Body request: TrackEventRequest): TrackEventResponse
}
```

#### Repository Implementation
```kotlin
@Singleton
class JobRepositoryImpl @Inject constructor(
    private val apiService: ApiService,
    private val jobDao: JobDao,
    private val deviceManager: DeviceManager
) : JobRepository {
    
    override suspend fun searchJobs(
        query: String,
        location: String?,
        limit: Int
    ): JobSearchResult {
        return try {
            val response = apiService.searchJobs(query, location, limit)
            if (response.success) {
                // Cache jobs locally
                jobDao.insertJobs(response.data.jobs.map { it.toEntity() })
                
                JobSearchResult(
                    jobs = response.data.jobs,
                    totalCount = response.data.totalCount,
                    hasMore = response.data.hasMore
                )
            } else {
                throw Exception(response.message ?: "Search failed")
            }
        } catch (e: Exception) {
            // Fallback to cached data
            val cachedJobs = jobDao.searchJobs("%$query%")
            JobSearchResult(
                jobs = cachedJobs.map { it.toDomain() },
                totalCount = cachedJobs.size,
                hasMore = false
            )
        }
    }
    
    override suspend fun saveJob(job: Job) {
        try {
            // Save to server
            val request = SaveJobRequest(
                jobId = job.id,
                deviceId = deviceManager.getDeviceId()
            )
            apiService.saveJob(request)
            
            // Save to local database
            jobDao.insertSavedJob(job.toSavedJobEntity())
        } catch (e: Exception) {
            // Save locally even if server fails
            jobDao.insertSavedJob(job.toSavedJobEntity())
            throw e
        }
    }
    
    override suspend fun getSavedJobs(): List<Job> {
        return try {
            val response = apiService.getSavedJobs()
            if (response.success) {
                response.data.jobs
            } else {
                // Fallback to local data
                jobDao.getSavedJobs().map { it.toDomain() }
            }
        } catch (e: Exception) {
            jobDao.getSavedJobs().map { it.toDomain() }
        }
    }
}
```

---

## Data Models

### **Domain Models**

#### Job.kt
```kotlin
data class Job(
    val id: Int,
    val title: String,
    val company: String,
    val location: String,
    val applyLink: String,
    val source: String,
    val postedAt: String,
    val description: String = "",
    val requirements: List<String> = emptyList(),
    val benefits: List<String> = emptyList(),
    val salary: Salary? = null,
    val jobType: JobType = JobType.FULL_TIME,
    val experienceLevel: ExperienceLevel = ExperienceLevel.MID_LEVEL,
    val isRemote: Boolean = false,
    val isSaved: Boolean = false
)

data class Salary(
    val min: Int?,
    val max: Int?,
    val currency: String = "USD",
    val period: SalaryPeriod = SalaryPeriod.YEARLY
)

enum class JobType {
    FULL_TIME, PART_TIME, CONTRACT, FREELANCE, INTERNSHIP
}

enum class ExperienceLevel {
    ENTRY_LEVEL, MID_LEVEL, SENIOR_LEVEL, EXECUTIVE
}

enum class SalaryPeriod {
    HOURLY, DAILY, WEEKLY, MONTHLY, YEARLY
}
```

#### Notification.kt
```kotlin
data class JobNotification(
    val id: String,
    val type: NotificationType,
    val title: String,
    val message: String,
    val matchedKeywords: List<String>,
    val jobCount: Int,
    val createdAt: String,
    val isRead: Boolean,
    val jobs: List<NotificationJob>
)

data class NotificationJob(
    val id: Int,
    val title: String,
    val company: String,
    val location: String,
    val applyLink: String,
    val postedAt: String,
    val source: String,
    val jobHash: String
)

enum class NotificationType {
    JOB_MATCH, BULK_JOB_MATCH, JOB_ALERT, SYSTEM
}
```

#### Analytics.kt
```kotlin
data class MarketOverview(
    val totalJobs: Int,
    val newJobsToday: Int,
    val totalCompanies: Int,
    val avgSalary: Double,
    val topLocations: List<LocationStat>,
    val topSkills: List<SkillStat>
)

data class KeywordTrend(
    val keyword: String,
    val jobCount: Int,
    val trend: Double, // Percentage change
    val chartData: List<ChartPoint>
)

data class CompanyAnalytic(
    val company: String,
    val jobCount: Int,
    val avgSalary: Double?,
    val locations: List<String>,
    val topSkills: List<String>
)

data class RemoteWorkAnalysis(
    val remoteJobsPercentage: Double,
    val hybridJobsPercentage: Double,
    val onSiteJobsPercentage: Double,
    val topRemoteSkills: List<String>,
    val remoteJobsTrend: List<ChartPoint>
)
```

---

## Services & Managers

### **Device Management**

#### DeviceManager.kt
```kotlin
@Singleton
class DeviceManager @Inject constructor(
    @ApplicationContext private val context: Context,
    private val preferencesManager: PreferencesManager
) {
    
    private val deviceId: String by lazy {
        preferencesManager.getDeviceId() ?: generateAndStoreDeviceId()
    }
    
    fun getDeviceId(): String = deviceId
    
    private fun generateAndStoreDeviceId(): String {
        val newId = UUID.randomUUID().toString()
        preferencesManager.saveDeviceId(newId)
        return newId
    }
    
    fun getDeviceInfo(): DeviceInfo {
        return DeviceInfo(
            deviceId = deviceId,
            platform = "android",
            osVersion = Build.VERSION.RELEASE,
            appVersion = getAppVersion(),
            model = "${Build.MANUFACTURER} ${Build.MODEL}",
            language = Locale.getDefault().language
        )
    }
    
    private fun getAppVersion(): String {
        return try {
            val packageInfo = context.packageManager.getPackageInfo(context.packageName, 0)
            packageInfo.versionName
        } catch (e: Exception) {
            "unknown"
        }
    }
}
```

### **Notification Manager**

#### NotificationManager.kt
```kotlin
@Singleton
class NotificationManager @Inject constructor(
    @ApplicationContext private val context: Context,
    private val preferencesManager: PreferencesManager
) {
    
    private val notificationManager = context.getSystemService(Context.NOTIFICATION_SERVICE) as android.app.NotificationManager
    
    init {
        createNotificationChannels()
    }
    
    private fun createNotificationChannels() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channels = listOf(
                NotificationChannel(
                    CHANNEL_JOB_MATCHES,
                    "Job Matches",
                    android.app.NotificationManager.IMPORTANCE_HIGH
                ).apply {
                    description = "Notifications for new job matches"
                    enableVibration(true)
                    setShowBadge(true)
                },
                
                NotificationChannel(
                    CHANNEL_JOB_ALERTS,
                    "Job Alerts",
                    android.app.NotificationManager.IMPORTANCE_DEFAULT
                ).apply {
                    description = "General job alerts and updates"
                },
                
                NotificationChannel(
                    CHANNEL_SYSTEM,
                    "System",
                    android.app.NotificationManager.IMPORTANCE_LOW
                ).apply {
                    description = "System notifications and updates"
                }
            )
            
            notificationManager.createNotificationChannels(channels)
        }
    }
    
    fun showJobMatchNotification(
        notificationId: String,
        title: String,
        message: String,
        jobCount: Int
    ) {
        val intent = createNotificationIntent(notificationId, NotificationType.JOB_MATCH)
        val pendingIntent = PendingIntent.getActivity(
            context, notificationId.hashCode(), intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
        
        val notification = NotificationCompat.Builder(context, CHANNEL_JOB_MATCHES)
            .setSmallIcon(R.drawable.ic_notification)
            .setContentTitle(title)
            .setContentText(message)
            .setNumber(jobCount)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setContentIntent(pendingIntent)
            .setAutoCancel(true)
            .addAction(
                R.drawable.ic_visibility,
                "View Jobs",
                pendingIntent
            )
            .setStyle(
                NotificationCompat.BigTextStyle()
                    .bigText(message)
                    .setBigContentTitle(title)
            )
            .build()
        
        notificationManager.notify(notificationId.hashCode(), notification)
        updateBadgeCount()
    }
    
    private fun createNotificationIntent(
        notificationId: String,
        type: NotificationType
    ): Intent {
        return Intent(context, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
            putExtra("notification_id", notificationId)
            putExtra("notification_type", type.name)
            putExtra("open_notifications", true)
        }
    }
    
    private fun updateBadgeCount() {
        // Update app badge count based on unread notifications
        // Implementation depends on launcher support
    }
    
    companion object {
        const val CHANNEL_JOB_MATCHES = "job_matches"
        const val CHANNEL_JOB_ALERTS = "job_alerts"
        const val CHANNEL_SYSTEM = "system"
    }
}
```

---

## UI/UX Implementation

### **Theme & Design System**

#### Theme.kt
```kotlin
private val DarkColorScheme = darkColorScheme(
    primary = Color(0xFF4CAF50),
    onPrimary = Color.White,
    primaryContainer = Color(0xFF2E7D32),
    onPrimaryContainer = Color.White,
    secondary = Color(0xFF81C784),
    onSecondary = Color.Black,
    background = Color(0xFF121212),
    surface = Color(0xFF1E1E1E),
    onBackground = Color.White,
    onSurface = Color.White,
    error = Color(0xFFCF6679)
)

private val LightColorScheme = lightColorScheme(
    primary = Color(0xFF4CAF50),
    onPrimary = Color.White,
    primaryContainer = Color(0xFFC8E6C9),
    onPrimaryContainer = Color(0xFF1B5E20),
    secondary = Color(0xFF66BB6A),
    onSecondary = Color.White,
    background = Color(0xFFFFFBFE),
    surface = Color.White,
    onBackground = Color(0xFF1C1B1F),
    onSurface = Color(0xFF1C1B1F),
    error = Color(0xFFBA1A1A)
)

@Composable
fun BirJobTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    val colorScheme = when {
        darkTheme -> DarkColorScheme
        else -> LightColorScheme
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}
```

### **Reusable Components**

#### JobCard.kt
```kotlin
@Composable
fun JobCard(
    job: Job,
    onJobClick: (Job) -> Unit,
    onApplyClick: (Job) -> Unit,
    onSaveClick: (Job) -> Unit,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier
            .fillMaxWidth()
            .clickable { onJobClick(job) },
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(
            modifier = Modifier.padding(16.dp)
        ) {
            // Job Title and Company
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.Top
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = job.title,
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis
                    )
                    
                    Text(
                        text = job.company,
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.primary,
                        modifier = Modifier.padding(top = 4.dp)
                    )
                }
                
                IconButton(
                    onClick = { onSaveClick(job) }
                ) {
                    Icon(
                        imageVector = if (job.isSaved) Icons.Filled.Bookmark else Icons.Outlined.BookmarkBorder,
                        contentDescription = "Save job",
                        tint = if (job.isSaved) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurface
                    )
                }
            }
            
            // Location and Job Type
            Row(
                modifier = Modifier.padding(top = 8.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(
                    imageVector = Icons.Default.LocationOn,
                    contentDescription = null,
                    modifier = Modifier.size(16.dp),
                    tint = MaterialTheme.colorScheme.onSurfaceVariant
                )
                
                Text(
                    text = job.location,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.padding(start = 4.dp)
                )
                
                if (job.isRemote) {
                    Chip(
                        text = "Remote",
                        modifier = Modifier.padding(start = 8.dp)
                    )
                }
            }
            
            // Salary if available
            job.salary?.let { salary ->
                Text(
                    text = formatSalary(salary),
                    style = MaterialTheme.typography.bodyMedium,
                    fontWeight = FontWeight.SemiBold,
                    color = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.padding(top = 4.dp)
                )
            }
            
            // Posted date and source
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(top = 8.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "Posted ${formatTimeAgo(job.postedAt)} • ${job.source}",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                
                Button(
                    onClick = { onApplyClick(job) },
                    modifier = Modifier.height(32.dp),
                    contentPadding = PaddingValues(horizontal = 16.dp, vertical = 4.dp)
                ) {
                    Text(
                        text = "Apply",
                        style = MaterialTheme.typography.labelMedium
                    )
                }
            }
        }
    }
}

@Composable
fun Chip(
    text: String,
    modifier: Modifier = Modifier
) {
    Surface(
        modifier = modifier,
        shape = RoundedCornerShape(12.dp),
        color = MaterialTheme.colorScheme.primaryContainer
    ) {
        Text(
            text = text,
            modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp),
            style = MaterialTheme.typography.labelSmall,
            color = MaterialTheme.colorScheme.onPrimaryContainer
        )
    }
}
```

---

## Navigation Flow

### **Navigation Setup**

#### Navigation.kt
```kotlin
@Composable
fun BirJobNavigation() {
    val navController = rememberNavController()
    
    NavHost(
        navController = navController,
        startDestination = "main"
    ) {
        composable("main") {
            MainScreen(navController = navController)
        }
        
        composable(
            "job_detail/{jobId}",
            arguments = listOf(navArgument("jobId") { type = NavType.IntType })
        ) { backStackEntry ->
            val jobId = backStackEntry.arguments?.getInt("jobId") ?: 0
            JobDetailScreen(
                jobId = jobId,
                onNavigateBack = { navController.popBackStack() }
            )
        }
        
        composable(
            "notification_detail/{notificationId}",
            arguments = listOf(navArgument("notificationId") { type = NavType.StringType })
        ) { backStackEntry ->
            val notificationId = backStackEntry.arguments?.getString("notificationId") ?: ""
            NotificationDetailScreen(
                notificationId = notificationId,
                onNavigateBack = { navController.popBackStack() }
            )
        }
        
        composable("settings") {
            SettingsScreen(
                onNavigateBack = { navController.popBackStack() }
            )
        }
    }
}

@Composable
fun MainScreen(navController: NavController) {
    var selectedTab by remember { mutableStateOf(0) }
    
    // Handle notification deep linking
    val context = LocalContext.current
    LaunchedEffect(Unit) {
        val intent = (context as? Activity)?.intent
        if (intent?.getBooleanExtra("open_notifications", false) == true) {
            selectedTab = 2 // Notifications tab
            
            val notificationId = intent.getStringExtra("notification_id")
            if (!notificationId.isNullOrEmpty()) {
                navController.navigate("notification_detail/$notificationId")
            }
        }
    }
    
    Scaffold(
        bottomBar = {
            NavigationBar {
                bottomNavItems.forEachIndexed { index, item ->
                    NavigationBarItem(
                        icon = { 
                            Icon(
                                imageVector = if (selectedTab == index) item.selectedIcon else item.unselectedIcon,
                                contentDescription = item.label
                            )
                        },
                        label = { Text(item.label) },
                        selected = selectedTab == index,
                        onClick = { selectedTab = index }
                    )
                }
            }
        }
    ) { paddingValues ->
        when (selectedTab) {
            0 -> JobSearchScreen(
                modifier = Modifier.padding(paddingValues),
                onJobClick = { job ->
                    navController.navigate("job_detail/${job.id}")
                }
            )
            1 -> AnalyticsScreen(modifier = Modifier.padding(paddingValues))
            2 -> NotificationInboxScreen(
                modifier = Modifier.padding(paddingValues),
                onNotificationClick = { notification ->
                    navController.navigate("notification_detail/${notification.id}")
                }
            )
            3 -> ChatScreen(modifier = Modifier.padding(paddingValues))
            4 -> ProfileScreen(
                modifier = Modifier.padding(paddingValues),
                onSettingsClick = { navController.navigate("settings") }
            )
        }
    }
}
```

---

## Push Notifications

### **FCM Implementation**

#### Firebase Setup (google-services.json)
```json
{
  "project_info": {
    "project_number": "YOUR_PROJECT_NUMBER",
    "project_id": "birjob-android",
    "storage_bucket": "birjob-android.appspot.com"
  },
  "client": [
    {
      "client_info": {
        "mobilesdk_app_id": "1:PROJECT_NUMBER:android:APP_ID",
        "android_client_info": {
          "package_name": "com.birjob.android"
        }
      },
      "oauth_client": [],
      "api_key": [
        {
          "current_key": "YOUR_API_KEY"
        }
      ],
      "services": {
        "appinvite_service": {
          "other_platform_oauth_client": []
        }
      }
    }
  ],
  "configuration_version": "1"
}
```

#### Notification Deep Linking
```kotlin
class MainActivity : ComponentActivity() {
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        handleNotificationIntent(intent)
        
        setContent {
            BirJobTheme {
                BirJobNavigation()
            }
        }
    }
    
    override fun onNewIntent(intent: Intent?) {
        super.onNewIntent(intent)
        intent?.let { handleNotificationIntent(it) }
    }
    
    private fun handleNotificationIntent(intent: Intent) {
        val notificationId = intent.getStringExtra("notification_id")
        val notificationType = intent.getStringExtra("notification_type")
        
        if (!notificationId.isNullOrEmpty()) {
            // Handle notification tap
            Log.d("MainActivity", "Opened from notification: $notificationId, type: $notificationType")
            
            // Set flag to open notifications screen
            intent.putExtra("open_notifications", true)
        }
    }
}
```

---

## Testing Strategy

### **Unit Tests**

#### ViewModelTest.kt
```kotlin
@ExperimentalCoroutinesTest
class JobSearchViewModelTest {
    
    @get:Rule
    val mainDispatcherRule = MainDispatcherRule()
    
    @Mock
    private lateinit var jobRepository: JobRepository
    
    @Mock
    private lateinit var analyticsRepository: AnalyticsRepository
    
    private lateinit var viewModel: JobSearchViewModel
    
    @Before
    fun setup() {
        MockitoAnnotations.openMocks(this)
        viewModel = JobSearchViewModel(jobRepository, analyticsRepository)
    }
    
    @Test
    fun `searchJobs should update jobs state`() = runTest {
        // Given
        val expectedJobs = listOf(
            Job(1, "Software Engineer", "Tech Corp", "Remote", "apply.com", "LinkedIn", "2024-01-01")
        )
        val searchResult = JobSearchResult(expectedJobs, 1, false)
        
        whenever(jobRepository.searchJobs("kotlin", null, 50)).thenReturn(searchResult)
        
        // When
        viewModel.searchJobs("kotlin")
        
        // Then
        assertEquals(expectedJobs, viewModel.jobs.value)
        assertFalse(viewModel.isLoading.value)
    }
    
    @Test
    fun `saveJob should call repository`() = runTest {
        // Given
        val job = Job(1, "Software Engineer", "Tech Corp", "Remote", "apply.com", "LinkedIn", "2024-01-01")
        
        // When
        viewModel.saveJob(job)
        
        // Then
        verify(jobRepository).saveJob(job)
    }
}
```

### **Integration Tests**

#### NotificationFlowTest.kt
```kotlin
@RunWith(AndroidJUnit4::class)
class NotificationFlowTest {
    
    @get:Rule
    val composeTestRule = createComposeRule()
    
    @Test
    fun notificationTap_opensCorrectScreen() {
        // Setup notification intent
        val intent = Intent().apply {
            putExtra("notification_id", "test-notification-123")
            putExtra("open_notifications", true)
        }
        
        // Launch activity with intent
        ActivityScenario.launch<MainActivity>(intent).use {
            // Verify notifications screen is displayed
            composeTestRule.onNodeWithText("Notifications").assertIsDisplayed()
            
            // Verify specific notification is highlighted or opened
            composeTestRule.onNodeWithText("test-notification-123").assertExists()
        }
    }
}
```

---

## Performance Optimization

### **Memory Management**
```kotlin
// Use appropriate list implementations
private val jobs = mutableStateListOf<Job>() // For Compose UI
private val jobsFlow = MutableStateFlow<List<Job>>(emptyList()) // For ViewModels

// Implement proper pagination
class JobPagingSource(
    private val apiService: ApiService,
    private val query: String
) : PagingSource<Int, Job>() {
    
    override suspend fun load(params: LoadParams<Int>): LoadResult<Int, Job> {
        return try {
            val page = params.key ?: 0
            val response = apiService.searchJobs(
                query = query,
                limit = params.loadSize,
                offset = page * params.loadSize
            )
            
            LoadResult.Page(
                data = response.data.jobs,
                prevKey = if (page == 0) null else page - 1,
                nextKey = if (response.data.hasMore) page + 1 else null
            )
        } catch (e: Exception) {
            LoadResult.Error(e)
        }
    }
    
    override fun getRefreshKey(state: PagingState<Int, Job>): Int? {
        return state.anchorPosition?.let { anchorPosition ->
            state.closestPageToPosition(anchorPosition)?.prevKey?.plus(1)
                ?: state.closestPageToPosition(anchorPosition)?.nextKey?.minus(1)
        }
    }
}
```

### **Network Optimization**
```kotlin
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {
    
    @Provides
    @Singleton
    fun provideOkHttpClient(): OkHttpClient {
        return OkHttpClient.Builder()
            .addInterceptor(HttpLoggingInterceptor().apply {
                level = if (BuildConfig.DEBUG) {
                    HttpLoggingInterceptor.Level.BODY
                } else {
                    HttpLoggingInterceptor.Level.NONE
                }
            })
            .addInterceptor(CacheInterceptor())
            .cache(Cache(File("cacheDir"), 10 * 1024 * 1024)) // 10MB cache
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .build()
    }
}

class CacheInterceptor : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val request = chain.request()
        val response = chain.proceed(request)
        
        // Cache GET requests for 5 minutes
        return if (request.method == "GET") {
            response.newBuilder()
                .header("Cache-Control", "public, max-age=300")
                .build()
        } else {
            response
        }
    }
}
```

---

## Deployment Guide

### **Build Configuration**

#### build.gradle (app level)
```gradle
android {
    compileSdk 34
    
    defaultConfig {
        applicationId "com.birjob.android"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0.0"
        
        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
        vectorDrawables {
            useSupportLibrary true
        }
    }
    
    buildTypes {
        debug {
            isDebuggable = true
            applicationIdSuffix = ".debug"
            versionNameSuffix = "-debug"
            buildConfigField "String", "API_BASE_URL", "\"https://your-dev-api.com/\""
            buildConfigField "boolean", "ENABLE_LOGGING", "true"
        }
        
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
            buildConfigField "String", "API_BASE_URL", "\"https://your-prod-api.com/\""
            buildConfigField "boolean", "ENABLE_LOGGING", "false"
        }
    }
    
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }
    
    kotlinOptions {
        jvmTarget = "1.8"
    }
    
    buildFeatures {
        compose = true
        buildConfig = true
    }
    
    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.8"
    }
    
    packaging {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
        }
    }
}
```

### **ProGuard Rules**
```proguard
# Keep data classes used for JSON serialization
-keep class com.birjob.android.data.remote.dto.** { *; }
-keep class com.birjob.android.domain.model.** { *; }

# Keep Retrofit interfaces
-keep interface com.birjob.android.data.remote.api.** { *; }

# Keep Firebase classes
-keep class com.google.firebase.** { *; }

# Keep Room classes
-keep class androidx.room.** { *; }
-keep class * extends androidx.room.RoomDatabase { *; }

# Keep Hilt generated classes
-keep class dagger.hilt.** { *; }
-keep class * extends dagger.hilt.android.HiltAndroidApp { *; }

# Keep custom exceptions
-keep class com.birjob.android.util.exceptions.** { *; }
```

### **Release Checklist**

1. **Code Quality**
   - [ ] All unit tests pass
   - [ ] Integration tests pass
   - [ ] Code review completed
   - [ ] No memory leaks detected
   - [ ] Performance testing completed

2. **Security**
   - [ ] API keys secured (not in code)
   - [ ] ProGuard rules applied
   - [ ] Network security config set
   - [ ] Permissions minimized

3. **Compatibility**
   - [ ] Tested on multiple Android versions (API 24-34)
   - [ ] Tested on different screen sizes
   - [ ] Tested on various device manufacturers
   - [ ] Accessibility features tested

4. **Backend Integration**
   - [ ] All API endpoints tested
   - [ ] Error handling implemented
   - [ ] Offline functionality works
   - [ ] Push notifications working

5. **Store Preparation**
   - [ ] App icons (all sizes)
   - [ ] Screenshots for Play Store
   - [ ] App description written
   - [ ] Privacy policy created
   - [ ] Terms of service created

### **Continuous Integration**

#### GitHub Actions (android.yml)
```yaml
name: Android CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up JDK 17
      uses: actions/setup-java@v3
      with:
        java-version: '17'
        distribution: 'temurin'
        
    - name: Grant execute permission for gradlew
      run: chmod +x gradlew
      
    - name: Run unit tests
      run: ./gradlew test
      
    - name: Run lint
      run: ./gradlew lint
      
    - name: Build debug APK
      run: ./gradlew assembleDebug
      
    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: debug-apk
        path: app/build/outputs/apk/debug/*.apk

  build-release:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up JDK 17
      uses: actions/setup-java@v3
      with:
        java-version: '17'
        distribution: 'temurin'
        
    - name: Build release APK
      run: ./gradlew assembleRelease
      env:
        KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
        KEY_ALIAS: ${{ secrets.KEY_ALIAS }}
        KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}
```

---

## Key Differences from iOS Version

### **Android-Specific Features**
1. **Material Design 3** instead of iOS Human Interface Guidelines
2. **Back button handling** with OnBackPressedDispatcher
3. **Android permissions** for notifications, storage, etc.
4. **Firebase Cloud Messaging** instead of APNs
5. **Google Play Store** deployment instead of App Store

### **Architecture Differences**
1. **MVVM + Repository** pattern (similar to iOS MVVM)
2. **Hilt for DI** instead of iOS manual DI
3. **Room Database** instead of Core Data
4. **Retrofit + OkHttp** instead of URLSession
5. **Jetpack Compose** instead of SwiftUI (similar declarative UI)

### **Backend Considerations**
You mentioned creating a separate backend for Android. Consider these endpoints that may need Android-specific handling:

1. **Device Registration**: Android device tokens (FCM) vs iOS (APNs)
2. **Push Notification Format**: FCM vs APNs payload differences
3. **Analytics Tracking**: Android-specific device info
4. **Deep Linking**: Android intent handling vs iOS URL schemes

---

## Next Steps

1. **Setup Development Environment**
   - Install Android Studio
   - Set up Firebase project
   - Configure Google Play Console

2. **Create Base Project**
   - Initialize Android project with dependencies
   - Set up navigation and theme
   - Implement basic architecture

3. **Implement Core Features**
   - Start with job search functionality
   - Add notification system
   - Implement analytics dashboard

4. **Backend Integration**
   - Create Android-specific API endpoints
   - Test push notifications
   - Implement offline functionality

5. **Testing & Optimization**
   - Write comprehensive tests
   - Optimize performance
   - Test on multiple devices

6. **Deployment**
   - Create release build
   - Upload to Google Play Store
   - Monitor analytics and crashes

This guide provides a complete roadmap for building the Android version of BirJob. Each section can be expanded further as you progress through development.
