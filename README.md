# BirJob Android Development Guide - COMPLETE IMPLEMENTATION

## Table of Contents
1. [Project Overview](#project-overview)
2. [Complete Development Environment Setup](#complete-development-environment-setup)
3. [Architecture & Technology Stack](#architecture--technology-stack)
4. [Detailed Project Structure](#detailed-project-structure)
5. [Database Layer - Complete Room Implementation](#database-layer---complete-room-implementation)
6. [Network Layer - Complete Retrofit Implementation](#network-layer---complete-retrofit-implementation)
7. [Repository Layer - Complete Implementation](#repository-layer---complete-implementation)
8. [Dependency Injection - Complete Hilt Setup](#dependency-injection---complete-hilt-setup)
9. [ViewModels - Complete Implementation](#viewmodels---complete-implementation)
10. [UI Layer - Complete Jetpack Compose Implementation](#ui-layer---complete-jetpack-compose-implementation)
11. [Complete Navigation Implementation](#complete-navigation-implementation)
12. [Push Notifications - Complete FCM Implementation](#push-notifications---complete-fcm-implementation)
13. [Background Services - Complete Implementation](#background-services---complete-implementation)
14. [Complete Analytics Implementation](#complete-analytics-implementation)
15. [Chat Feature - Complete Implementation](#chat-feature---complete-implementation)
16. [Complete Testing Implementation](#complete-testing-implementation)
17. [Security & Privacy - Complete Implementation](#security--privacy---complete-implementation)
18. [Performance Optimization - Detailed Implementation](#performance-optimization---detailed-implementation)
19. [Complete CI/CD Pipeline](#complete-cicd-pipeline)
20. [Deployment - Complete Guide](#deployment---complete-guide)
21. [Monitoring & Crashlytics](#monitoring--crashlytics)
22. [Complete Feature Comparison iOS vs Android](#complete-feature-comparison-ios-vs-android)

---

## Project Overview

**App Name**: BirJob (Android Version)  
**Package Name**: `com.birjob.android`  
**Platform**: Android (Kotlin)  
**Minimum SDK**: API 24 (Android 7.0) - 87% market coverage  
**Target SDK**: API 34 (Android 14)  
**Architecture**: Clean Architecture + MVVM + Repository Pattern  
**UI Framework**: Jetpack Compose  
**Backend**: REST API with Firebase integration  

### Complete Feature Set
```
Core Features:
├── 🔍 Job Search & Filtering
│   ├── Real-time search with debouncing
│   ├── Advanced filters (location, salary, remote, etc.)
│   ├── Search history and suggestions
│   └── Save/unsave jobs functionality
├── 🔔 Smart Notification System
│   ├── FCM push notifications
│   ├── Notification inbox with categorization
│   ├── Mark as read/unread functionality
│   ├── Bulk operations (mark all as read, delete)
│   └── Deep linking from notifications
├── 📊 Analytics Dashboard
│   ├── Market overview with real-time stats
│   ├── Keyword trends with interactive charts
│   ├── Company analytics and insights
│   ├── Remote work analysis
│   └── Personal job search analytics
├── 🤖 AI Chat Assistant
│   ├── Job recommendations
│   ├── Career advice
│   ├── Resume feedback
│   └── Interview preparation
├── 👤 Profile Management
│   ├── User preferences
│   ├── Keyword management
│   ├── Notification settings
│   └── Privacy controls
└── 🎨 Adaptive UI
    ├── Material Design 3
    ├── Dark/Light theme
    ├── Dynamic colors (Android 12+)
    └── Responsive design for tablets
```

---

## Complete Development Environment Setup

### **Step 1: Install Required Software**

#### Android Studio Installation
```bash
# Download Android Studio from: https://developer.android.com/studio
# Install with these components:
- Android SDK Platform 34
- Android SDK Build-Tools 34.0.0
- Android Emulator
- Intel x86 Emulator Accelerator (HAXM installer)
- Google Play services
- Google Repository
```

#### SDK Configuration
```bash
# Set ANDROID_HOME environment variable
export ANDROID_HOME=$HOME/Library/Android/sdk  # macOS
export ANDROID_HOME=$HOME/Android/Sdk          # Linux
set ANDROID_HOME=C:\Users\%USERNAME%\AppData\Local\Android\Sdk  # Windows

# Add to PATH
export PATH=$PATH:$ANDROID_HOME/emulator
export PATH=$PATH:$ANDROID_HOME/tools
export PATH=$PATH:$ANDROID_HOME/tools/bin
export PATH=$PATH:$ANDROID_HOME/platform-tools
```

#### Required SDK Components
```bash
# Install via SDK Manager or command line:
sdkmanager "platforms;android-34"
sdkmanager "platforms;android-24"  # Minimum supported
sdkmanager "build-tools;34.0.0"
sdkmanager "extras;google;google_play_services"
sdkmanager "extras;google;m2repository"
sdkmanager "extras;android;m2repository"
```

### **Step 2: Create New Project**

#### Project Creation Script
```bash
# Create new project directory
mkdir BirJobAndroid && cd BirJobAndroid

# Initialize git
git init
git remote add origin https://github.com/yourusername/birjob-android.git

# Create basic project structure
mkdir -p app/src/main/java/com/birjob/android
mkdir -p app/src/main/res
mkdir -p app/src/test/java/com/birjob/android
mkdir -p app/src/androidTest/java/com/birjob/android
```

#### settings.gradle.kts
```kotlin
pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}

dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
        maven { url = uri("https://jitpack.io") }
    }
}

rootProject.name = "BirJob"
include(":app")
```

#### Project-level build.gradle.kts
```kotlin
buildscript {
    extra.apply {
        set("compose_version", "1.5.8")
        set("compose_compiler_version", "1.5.8")
        set("kotlin_version", "1.9.22")
        set("hilt_version", "2.48")
        set("room_version", "2.6.1")
        set("retrofit_version", "2.9.0")
        set("okhttp_version", "4.12.0")
        set("lifecycle_version", "2.7.0")
        set("navigation_version", "2.7.6")
    }
}

plugins {
    id("com.android.application") version "8.2.2" apply false
    id("org.jetbrains.kotlin.android") version "1.9.22" apply false
    id("com.google.dagger.hilt.android") version "2.48" apply false
    id("com.google.gms.google-services") version "4.4.0" apply false
    id("com.google.firebase.crashlytics") version "2.9.9" apply false
    id("kotlin-parcelize") apply false
    id("org.jetbrains.kotlin.plugin.serialization") version "1.9.22" apply false
}
```

### **Step 3: Complete App-level Configuration**

#### app/build.gradle.kts (Complete Configuration)
```kotlin
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("kotlin-kapt")
    id("kotlin-parcelize")
    id("dagger.hilt.android.plugin")
    id("com.google.gms.google-services")
    id("com.google.firebase.crashlytics")
    id("org.jetbrains.kotlin.plugin.serialization")
}

android {
    namespace = "com.birjob.android"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.birjob.android"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0.0"

        testInstrumentationRunner = "com.birjob.android.CustomTestRunner"
        vectorDrawables {
            useSupportLibrary = true
        }

        // Room schema export
        kapt {
            arguments {
                arg("room.schemaLocation", "$projectDir/schemas")
            }
        }

        buildConfigField("String", "VERSION_NAME", "\"${defaultConfig.versionName}\"")
        buildConfigField("int", "VERSION_CODE", "${defaultConfig.versionCode}")
    }

    buildTypes {
        debug {
            isDebuggable = true
            applicationIdSuffix = ".debug"
            versionNameSuffix = "-debug"
            buildConfigField("String", "API_BASE_URL", "\"https://birjob-backend-dev.herokuapp.com/\"")
            buildConfigField("String", "WEBSOCKET_URL", "\"wss://birjob-backend-dev.herokuapp.com/ws\"")
            buildConfigField("boolean", "ENABLE_LOGGING", "true")
            buildConfigField("boolean", "ENABLE_CRASH_REPORTING", "false")
            isMinifyEnabled = false
            isShrinkResources = false
        }

        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
            buildConfigField("String", "API_BASE_URL", "\"https://birjob-backend.herokuapp.com/\"")
            buildConfigField("String", "WEBSOCKET_URL", "\"wss://birjob-backend.herokuapp.com/ws\"")
            buildConfigField("boolean", "ENABLE_LOGGING", "false")
            buildConfigField("boolean", "ENABLE_CRASH_REPORTING", "true")

            signingConfig = signingConfigs.getByName("debug") // Replace with actual signing config
        }

        create("staging") {
            initWith(getByName("debug"))
            applicationIdSuffix = ".staging"
            versionNameSuffix = "-staging"
            buildConfigField("String", "API_BASE_URL", "\"https://birjob-backend-staging.herokuapp.com/\"")
            buildConfigField("boolean", "ENABLE_LOGGING", "true")
            buildConfigField("boolean", "ENABLE_CRASH_REPORTING", "true")
            isMinifyEnabled = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
        isCoreLibraryDesugaringEnabled = true
    }

    kotlinOptions {
        jvmTarget = "1.8"
        freeCompilerArgs += listOf(
            "-opt-in=androidx.compose.material3.ExperimentalMaterial3Api",
            "-opt-in=androidx.compose.foundation.ExperimentalFoundationApi",
            "-opt-in=androidx.compose.animation.ExperimentalAnimationApi",
            "-opt-in=kotlinx.coroutines.ExperimentalCoroutinesApi",
            "-opt-in=androidx.compose.ui.ExperimentalComposeUiApi"
        )
    }

    buildFeatures {
        compose = true
        buildConfig = true
    }

    composeOptions {
        kotlinCompilerExtensionVersion = rootProject.extra["compose_compiler_version"] as String
    }

    packaging {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
            excludes += "/META-INF/gradle/incremental.annotation.processors"
        }
    }

    testOptions {
        unitTests {
            isIncludeAndroidResources = true
            isReturnDefaultValues = true
        }
        
        compileOptions {
            sourceCompatibility = JavaVersion.VERSION_1_8
            targetCompatibility = JavaVersion.VERSION_1_8
        }
    }
}

dependencies {
    val composeVersion = rootProject.extra["compose_version"] as String
    val hiltVersion = rootProject.extra["hilt_version"] as String
    val roomVersion = rootProject.extra["room_version"] as String
    val retrofitVersion = rootProject.extra["retrofit_version"] as String
    val okhttpVersion = rootProject.extra["okhttp_version"] as String
    val lifecycleVersion = rootProject.extra["lifecycle_version"] as String
    val navigationVersion = rootProject.extra["navigation_version"] as String

    // Core Android Dependencies
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:$lifecycleVersion")
    implementation("androidx.activity:activity-compose:1.8.2")
    implementation("androidx.core:core-splashscreen:1.0.1")
    coreLibraryDesugaring("com.android.tools:desugar_jdk_libs:2.0.4")

    // Compose BOM - ensures all compose libraries use compatible versions
    implementation(platform("androidx.compose:compose-bom:2024.02.00"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.material3:material3-window-size-class")
    implementation("androidx.compose.material:material-icons-extended")
    implementation("androidx.compose.animation:animation")
    implementation("androidx.compose.foundation:foundation")
    implementation("androidx.compose.runtime:runtime-livedata")

    // Navigation Compose
    implementation("androidx.navigation:navigation-compose:$navigationVersion")
    implementation("androidx.navigation:navigation-runtime-ktx:$navigationVersion")

    // ViewModel Compose
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:$lifecycleVersion")
    implementation("androidx.lifecycle:lifecycle-runtime-compose:$lifecycleVersion")

    // Hilt Dependency Injection
    implementation("com.google.dagger:hilt-android:$hiltVersion")
    kapt("com.google.dagger:hilt-compiler:$hiltVersion")
    implementation("androidx.hilt:hilt-navigation-compose:1.1.0")
    implementation("androidx.hilt:hilt-work:1.1.0")
    kapt("androidx.hilt:hilt-compiler:1.1.0")

    // Networking
    implementation("com.squareup.retrofit2:retrofit:$retrofitVersion")
    implementation("com.squareup.retrofit2:converter-gson:$retrofitVersion")
    implementation("com.squareup.retrofit2:converter-kotlinx-serialization:1.0.0")
    implementation("com.squareup.okhttp3:okhttp:$okhttpVersion")
    implementation("com.squareup.okhttp3:logging-interceptor:$okhttpVersion")
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.2")

    // Room Database
    implementation("androidx.room:room-runtime:$roomVersion")
    implementation("androidx.room:room-ktx:$roomVersion")
    kapt("androidx.room:room-compiler:$roomVersion")
    implementation("androidx.room:room-paging:$roomVersion")

    // Paging 3
    implementation("androidx.paging:paging-runtime-ktx:3.2.1")
    implementation("androidx.paging:paging-compose:3.2.1")

    // DataStore (for preferences)
    implementation("androidx.datastore:datastore-preferences:1.0.0")

    // Work Manager
    implementation("androidx.work:work-runtime-ktx:2.9.0")

    // Firebase
    implementation(platform("com.google.firebase:firebase-bom:32.7.0"))
    implementation("com.google.firebase:firebase-messaging-ktx")
    implementation("com.google.firebase:firebase-analytics-ktx")
    implementation("com.google.firebase:firebase-crashlytics-ktx")
    implementation("com.google.firebase:firebase-config-ktx")

    // Image Loading
    implementation("io.coil-kt:coil-compose:2.5.0")

    // Charts for Analytics
    implementation("com.github.PhilJay:MPAndroidChart:v3.1.0")
    implementation("co.yml:ycharts:2.1.0")

    // WebView
    implementation("androidx.webkit:webkit:1.9.0")
    implementation("com.google.accompanist:accompanist-webview:0.32.0")

    // Date/Time
    implementation("org.jetbrains.kotlinx:kotlinx-datetime:0.5.0")

    // Permissions
    implementation("com.google.accompanist:accompanist-permissions:0.32.0")

    // System UI Controller
    implementation("com.google.accompanist:accompanist-systemuicontroller:0.32.0")

    // Lottie Animations
    implementation("com.airbnb.android:lottie-compose:6.3.0")

    // Timber Logging
    implementation("com.jakewharton.timber:timber:5.0.1")

    // Testing Dependencies
    testImplementation("junit:junit:4.13.2")
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.7.3")
    testImplementation("androidx.arch.core:core-testing:2.2.0")
    testImplementation("com.google.truth:truth:1.1.4")
    testImplementation("org.mockito:mockito-core:5.8.0")
    testImplementation("org.mockito.kotlin:mockito-kotlin:5.2.1")
    testImplementation("androidx.room:room-testing:$roomVersion")
    testImplementation("com.squareup.okhttp3:mockwebserver:$okhttpVersion")
    testImplementation("androidx.work:work-testing:2.9.0")

    // Android Instrumentation Testing
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1")
    androidTestImplementation("androidx.test.espresso:espresso-intents:3.5.1")
    androidTestImplementation("androidx.compose.ui:ui-test-junit4")
    androidTestImplementation("androidx.navigation:navigation-testing:$navigationVersion")
    androidTestImplementation("com.google.dagger:hilt-android-testing:$hiltVersion")
    kaptAndroidTest("com.google.dagger:hilt-compiler:$hiltVersion")
    androidTestImplementation("androidx.work:work-testing:2.9.0")

    // Debug Tools
    debugImplementation("androidx.compose.ui:ui-tooling")
    debugImplementation("androidx.compose.ui:ui-test-manifest")
    debugImplementation("com.squareup.leakcanary:leakcanary-android:2.12")
}
```

---

## Database Layer - Complete Room Implementation

### **Complete Database Schema**

#### Entity Definitions

##### JobEntity.kt
```kotlin
@Entity(
    tableName = "jobs",
    indices = [
        Index(value = ["title"]),
        Index(value = ["company"]),
        Index(value = ["location"]),
        Index(value = ["source"]),
        Index(value = ["posted_at"]),
        Index(value = ["is_remote"]),
        Index(value = ["created_at"])
    ]
)
data class JobEntity(
    @PrimaryKey
    @ColumnInfo(name = "id")
    val id: Int,
    
    @ColumnInfo(name = "title")
    val title: String,
    
    @ColumnInfo(name = "company")
    val company: String,
    
    @ColumnInfo(name = "location")
    val location: String,
    
    @ColumnInfo(name = "apply_link")
    val applyLink: String,
    
    @ColumnInfo(name = "source")
    val source: String,
    
    @ColumnInfo(name = "posted_at")
    val postedAt: String,
    
    @ColumnInfo(name = "description")
    val description: String = "",
    
    @ColumnInfo(name = "requirements")
    val requirements: String = "", // JSON string
    
    @ColumnInfo(name = "benefits")
    val benefits: String = "", // JSON string
    
    @ColumnInfo(name = "salary_min")
    val salaryMin: Int? = null,
    
    @ColumnInfo(name = "salary_max")
    val salaryMax: Int? = null,
    
    @ColumnInfo(name = "salary_currency")
    val salaryCurrency: String = "USD",
    
    @ColumnInfo(name = "salary_period")
    val salaryPeriod: String = "YEARLY",
    
    @ColumnInfo(name = "job_type")
    val jobType: String = "FULL_TIME",
    
    @ColumnInfo(name = "experience_level")
    val experienceLevel: String = "MID_LEVEL",
    
    @ColumnInfo(name = "is_remote")
    val isRemote: Boolean = false,
    
    @ColumnInfo(name = "created_at")
    val createdAt: Long = System.currentTimeMillis(),
    
    @ColumnInfo(name = "updated_at")
    val updatedAt: Long = System.currentTimeMillis()
)
```

##### SavedJobEntity.kt
```kotlin
@Entity(
    tableName = "saved_jobs",
    indices = [
        Index(value = ["job_id"], unique = true),
        Index(value = ["saved_at"])
    ]
)
data class SavedJobEntity(
    @PrimaryKey(autoGenerate = true)
    @ColumnInfo(name = "id")
    val id: Long = 0,
    
    @ColumnInfo(name = "job_id")
    val jobId: Int,
    
    @ColumnInfo(name = "saved_at")
    val savedAt: Long = System.currentTimeMillis(),
    
    @ColumnInfo(name = "notes")
    val notes: String = ""
)
```

##### NotificationEntity.kt
```kotlin
@Entity(
    tableName = "notifications",
    indices = [
        Index(value = ["notification_id"], unique = true),
        Index(value = ["type"]),
        Index(value = ["is_read"]),
        Index(value = ["created_at"])
    ]
)
data class NotificationEntity(
    @PrimaryKey(autoGenerate = true)
    @ColumnInfo(name = "id")
    val id: Long = 0,
    
    @ColumnInfo(name = "notification_id")
    val notificationId: String,
    
    @ColumnInfo(name = "type")
    val type: String,
    
    @ColumnInfo(name = "title")
    val title: String,
    
    @ColumnInfo(name = "message")
    val message: String,
    
    @ColumnInfo(name = "matched_keywords")
    val matchedKeywords: String, // JSON array
    
    @ColumnInfo(name = "job_count")
    val jobCount: Int,
    
    @ColumnInfo(name = "jobs_data")
    val jobsData: String, // JSON array of jobs
    
    @ColumnInfo(name = "is_read")
    val isRead: Boolean = false,
    
    @ColumnInfo(name = "created_at")
    val createdAt: String,
    
    @ColumnInfo(name = "received_at")
    val receivedAt: Long = System.currentTimeMillis()
)
```

##### SearchHistoryEntity.kt
```kotlin
@Entity(
    tableName = "search_history",
    indices = [
        Index(value = ["query"]),
        Index(value = ["searched_at"]),
        Index(value = ["result_count"])
    ]
)
data class SearchHistoryEntity(
    @PrimaryKey(autoGenerate = true)
    @ColumnInfo(name = "id")
    val id: Long = 0,
    
    @ColumnInfo(name = "query")
    val query: String,
    
    @ColumnInfo(name = "location")
    val location: String? = null,
    
    @ColumnInfo(name = "result_count")
    val resultCount: Int,
    
    @ColumnInfo(name = "searched_at")
    val searchedAt: Long = System.currentTimeMillis()
)
```

### **Complete DAO Implementations**

#### JobDao.kt
```kotlin
@Dao
interface JobDao {
    
    // Basic CRUD Operations
    @Query("SELECT * FROM jobs WHERE id = :jobId")
    suspend fun getJobById(jobId: Int): JobEntity?
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertJob(job: JobEntity)
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertJobs(jobs: List<JobEntity>)
    
    @Update
    suspend fun updateJob(job: JobEntity)
    
    @Delete
    suspend fun deleteJob(job: JobEntity)
    
    @Query("DELETE FROM jobs WHERE id = :jobId")
    suspend fun deleteJobById(jobId: Int)
    
    // Search Operations
    @Query("""
        SELECT * FROM jobs 
        WHERE (:query IS NULL OR title LIKE '%' || :query || '%' 
               OR company LIKE '%' || :query || '%'
               OR description LIKE '%' || :query || '%')
        AND (:location IS NULL OR location LIKE '%' || :location || '%')
        AND (:isRemote IS NULL OR is_remote = :isRemote)
        AND (:jobType IS NULL OR job_type = :jobType)
        AND (:minSalary IS NULL OR salary_min >= :minSalary)
        AND (:maxSalary IS NULL OR salary_max <= :maxSalary)
        ORDER BY posted_at DESC, created_at DESC
        LIMIT :limit OFFSET :offset
    """)
    suspend fun searchJobs(
        query: String?,
        location: String?,
        isRemote: Boolean?,
        jobType: String?,
        minSalary: Int?,
        maxSalary: Int?,
        limit: Int,
        offset: Int
    ): List<JobEntity>
    
    @Query("""
        SELECT COUNT(*) FROM jobs 
        WHERE (:query IS NULL OR title LIKE '%' || :query || '%' 
               OR company LIKE '%' || :query || '%'
               OR description LIKE '%' || :query || '%')
        AND (:location IS NULL OR location LIKE '%' || :location || '%')
        AND (:isRemote IS NULL OR is_remote = :isRemote)
        AND (:jobType IS NULL OR job_type = :jobType)
        AND (:minSalary IS NULL OR salary_min >= :minSalary)
        AND (:maxSalary IS NULL OR salary_max <= :maxSalary)
    """)
    suspend fun getSearchResultCount(
        query: String?,
        location: String?,
        isRemote: Boolean?,
        jobType: String?,
        minSalary: Int?,
        maxSalary: Int?
    ): Int
    
    // Saved Jobs Operations
    @Query("""
        SELECT j.* FROM jobs j
        INNER JOIN saved_jobs s ON j.id = s.job_id
        ORDER BY s.saved_at DESC
    """)
    suspend fun getSavedJobs(): List<JobEntity>
    
    @Query("""
        SELECT j.* FROM jobs j
        INNER JOIN saved_jobs s ON j.id = s.job_id
        ORDER BY s.saved_at DESC
    """)
    fun getSavedJobsPaged(): PagingSource<Int, JobEntity>
    
    @Query("SELECT COUNT(*) FROM saved_jobs")
    suspend fun getSavedJobsCount(): Int
    
    @Query("SELECT EXISTS(SELECT 1 FROM saved_jobs WHERE job_id = :jobId)")
    suspend fun isJobSaved(jobId: Int): Boolean
    
    // Analytics Queries
    @Query("SELECT company, COUNT(*) as count FROM jobs GROUP BY company ORDER BY count DESC LIMIT :limit")
    suspend fun getTopCompaniesByJobCount(limit: Int): List<CompanyJobCount>
    
    @Query("SELECT location, COUNT(*) as count FROM jobs GROUP BY location ORDER BY count DESC LIMIT :limit")
    suspend fun getTopLocationsByJobCount(limit: Int): List<LocationJobCount>
    
    @Query("SELECT job_type, COUNT(*) as count FROM jobs GROUP BY job_type ORDER BY count DESC")
    suspend fun getJobTypeDistribution(): List<JobTypeCount>
    
    @Query("SELECT COUNT(*) FROM jobs WHERE is_remote = 1")
    suspend fun getRemoteJobsCount(): Int
    
    @Query("SELECT COUNT(*) FROM jobs")
    suspend fun getTotalJobsCount(): Int
    
    @Query("SELECT AVG(salary_min) FROM jobs WHERE salary_min IS NOT NULL")
    suspend fun getAverageSalary(): Double?
    
    // Cleanup Operations
    @Query("DELETE FROM jobs WHERE created_at < :timestamp")
    suspend fun deleteJobsOlderThan(timestamp: Long)
    
    @Query("SELECT COUNT(*) FROM jobs")
    suspend fun getJobCount(): Int
    
    // Recent Jobs
    @Query("SELECT * FROM jobs ORDER BY created_at DESC LIMIT :limit")
    suspend fun getRecentJobs(limit: Int): List<JobEntity>
}

// Helper data classes for analytics
data class CompanyJobCount(val company: String, val count: Int)
data class LocationJobCount(val location: String, val count: Int)
data class JobTypeCount(val jobType: String, val count: Int)
```

#### SavedJobDao.kt
```kotlin
@Dao
interface SavedJobDao {
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertSavedJob(savedJob: SavedJobEntity)
    
    @Query("DELETE FROM saved_jobs WHERE job_id = :jobId")
    suspend fun deleteSavedJob(jobId: Int)
    
    @Query("SELECT * FROM saved_jobs ORDER BY saved_at DESC")
    suspend fun getAllSavedJobs(): List<SavedJobEntity>
    
    @Query("SELECT * FROM saved_jobs WHERE job_id = :jobId")
    suspend fun getSavedJob(jobId: Int): SavedJobEntity?
    
    @Query("SELECT EXISTS(SELECT 1 FROM saved_jobs WHERE job_id = :jobId)")
    suspend fun isJobSaved(jobId: Int): Boolean
    
    @Query("SELECT COUNT(*) FROM saved_jobs")
    suspend fun getSavedJobsCount(): Int
    
    @Query("DELETE FROM saved_jobs")
    suspend fun deleteAllSavedJobs()
    
    @Update
    suspend fun updateSavedJob(savedJob: SavedJobEntity)
}
```

#### NotificationDao.kt
```kotlin
@Dao
interface NotificationDao {
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertNotification(notification: NotificationEntity)
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertNotifications(notifications: List<NotificationEntity>)
    
    @Query("SELECT * FROM notifications ORDER BY received_at DESC")
    suspend fun getAllNotifications(): List<NotificationEntity>
    
    @Query("SELECT * FROM notifications ORDER BY received_at DESC LIMIT :limit OFFSET :offset")
    suspend fun getNotificationsPaged(limit: Int, offset: Int): List<NotificationEntity>
    
    @Query("SELECT * FROM notifications ORDER BY received_at DESC")
    fun getNotificationsPagingSource(): PagingSource<Int, NotificationEntity>
    
    @Query("SELECT * FROM notifications WHERE notification_id = :notificationId")
    suspend fun getNotificationById(notificationId: String): NotificationEntity?
    
    @Query("UPDATE notifications SET is_read = 1 WHERE notification_id = :notificationId")
    suspend fun markNotificationAsRead(notificationId: String)
    
    @Query("UPDATE notifications SET is_read = 1")
    suspend fun markAllNotificationsAsRead()
    
    @Query("SELECT COUNT(*) FROM notifications WHERE is_read = 0")
    suspend fun getUnreadNotificationsCount(): Int
    
    @Query("SELECT COUNT(*) FROM notifications")
    suspend fun getTotalNotificationsCount(): Int
    
    @Query("DELETE FROM notifications WHERE notification_id = :notificationId")
    suspend fun deleteNotification(notificationId: String)
    
    @Query("DELETE FROM notifications")
    suspend fun deleteAllNotifications()
    
    @Query("SELECT * FROM notifications WHERE is_read = 0 ORDER BY received_at DESC")
    suspend fun getUnreadNotifications(): List<NotificationEntity>
    
    @Query("SELECT * FROM notifications WHERE type = :type ORDER BY received_at DESC")
    suspend fun getNotificationsByType(type: String): List<NotificationEntity>
    
    @Query("DELETE FROM notifications WHERE received_at < :timestamp")
    suspend fun deleteNotificationsOlderThan(timestamp: Long)
}
```

#### SearchHistoryDao.kt
```kotlin
@Dao
interface SearchHistoryDao {
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertSearchHistory(searchHistory: SearchHistoryEntity)
    
    @Query("SELECT * FROM search_history ORDER BY searched_at DESC LIMIT :limit")
    suspend fun getRecentSearches(limit: Int = 10): List<SearchHistoryEntity>
    
    @Query("SELECT DISTINCT query FROM search_history WHERE query LIKE :query || '%' ORDER BY searched_at DESC LIMIT :limit")
    suspend fun getSearchSuggestions(query: String, limit: Int = 5): List<String>
    
    @Query("DELETE FROM search_history WHERE id = :id")
    suspend fun deleteSearchHistory(id: Long)
    
    @Query("DELETE FROM search_history")
    suspend fun deleteAllSearchHistory()
    
    @Query("SELECT COUNT(*) FROM search_history")
    suspend fun getSearchHistoryCount(): Int
    
    @Query("DELETE FROM search_history WHERE searched_at < :timestamp")
    suspend fun deleteSearchHistoryOlderThan(timestamp: Long)
    
    @Query("SELECT AVG(result_count) FROM search_history")
    suspend fun getAverageSearchResultCount(): Double
}
```

### **Database Configuration**

#### BirJobDatabase.kt
```kotlin
@Database(
    entities = [
        JobEntity::class,
        SavedJobEntity::class,
        NotificationEntity::class,
        SearchHistoryEntity::class
    ],
    version = 1,
    exportSchema = true,
    autoMigrations = []
)
@TypeConverters(Converters::class)
abstract class BirJobDatabase : RoomDatabase() {
    
    abstract fun jobDao(): JobDao
    abstract fun savedJobDao(): SavedJobDao
    abstract fun notificationDao(): NotificationDao
    abstract fun searchHistoryDao(): SearchHistoryDao
    
    companion object {
        const val DATABASE_NAME = "birjob_database"
    }
}
```

#### Type Converters
```kotlin
class Converters {
    
    private val gson = Gson()
    
    @TypeConverter
    fun fromStringList(value: List<String>): String {
        return gson.toJson(value)
    }
    
    @TypeConverter
    fun toStringList(value: String): List<String> {
        return try {
            gson.fromJson(value, object : TypeToken<List<String>>() {}.type)
        } catch (e: Exception) {
            emptyList()
        }
    }
    
    @TypeConverter
    fun fromDate(date: Date?): Long? {
        return date?.time
    }
    
    @TypeConverter
    fun toDate(timestamp: Long?): Date? {
        return timestamp?.let { Date(it) }
    }
}
```

This is just the beginning of a much more detailed guide. Would you like me to continue expanding it with more comprehensive implementation details for the remaining sections?

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
