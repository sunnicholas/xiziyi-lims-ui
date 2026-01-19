---
name: "xiziyi-gas-process"
description: "Comprehensive UI design summary for the Cylinder (Gas) Business Process, covering Business Acceptance, Sample Management, Task Assignment, and Record Entry."
---

# Cylinder Business Process UI Design Summary

This document summarizes the user interface design patterns and flows for the "Cylinder (Gas)" business process in the Xiziyi LIMS system.

## 1. Global Layout & Navigation
-   **Sidebar**: Fixed left navigation menu with clear icons for each module (Business, Sample, Assign, Record, Report).
-   **Navbar**: Top bar containing:
    -   **Breadcrumbs**: Indicates current page location (e.g., "Home / Sample Management").
    -   **Update Time**: Automatically updated timestamp (e.g., `(更新时间：2026-01-19 17:15:00)`) to track version freshness.
    -   **User Profile**: Dropdown for user actions (Logout, etc.).
-   **Container**: `app-container` with white background, padding, and shadow for content isolation.

## 2. Business Acceptance (业务受理)
*File: `preview_business.html`*

-   **Goal**: Initiate new testing requests (Entrusts).
-   **UI Pattern**: Step-based Wizard or Type Selection + Form.
-   **Key Features**:
    -   **Device Type Selection**: Visual cards (`type-card`) with icons to select the specific cylinder type (e.g., Seamless, Welded, Safety Valve).
    -   **Step Form**: Logical progression:
        1.  **Client Info**: Company name, contact details.
        2.  **Device Details**: Specifications, quantities.
        3.  **Confirmation**: Review and submit.
    -   **Validation**: Required fields marked with red asterisks; real-time validation.

## 3. Sample Management (样品管理)
*File: `preview_sample.html`*

-   **Goal**: Track physical samples from receipt to return.
-   **UI Pattern**: Data Table with Expandable Rows.
-   **Key Features**:
    -   **Search Bar**: Filter by Entrust No, Company, Status.
    -   **Expandable Rows**:
        -   **Parent Row**: Entrust Order summary (Entrust No, Client, Total Qty).
        -   **Child Row (Expanded)**: List of individual devices/cylinders within that order.
    -   **Status Tags**: Color-coded tags (e.g., `待签收` (Warning), `已签收` (Success)).
    -   **Actions**:
        -   **Receive (签收)**: Updates status to "Received".
        -   **Print Label (打印标签)**: Generates QR/Barcode for the sample.

## 4. Task Assignment (任务分配)
*File: `preview_assign.html`*

-   **Goal**: Assign received samples to specific inspectors/testers.
-   **UI Pattern**: List View with Assignment Modals.
-   **Key Features**:
    -   **Pending List**: Shows samples ready for testing (Status = Received).
    -   **Assignment Action**:
        -   Click "Assign" to open a dialog.
        -   Select **Tester** (Inspector) and **Reviewer** (Auditor).
    -   **Batch Assignment**: Checkbox selection to assign multiple samples to one tester simultaneously.

## 5. Original Records (原始记录)
*File: `preview_record.html`*

-   **Goal**: Input detailed technical inspection data.
-   **UI Pattern**: Header + Tabbed Form.
-   **Key Features**:
    -   **Unified Header**: Critical identifier info (Cylinder No, Specs) displayed *once* at the top (pinned), avoiding repetition inside tabs.
    -   **Top-Level Tabs**: Flat hierarchy for quick switching between inspection phases:
        -   *Visual (外观)*, *Internal (内部)*, *Bottle Mouth (瓶口)*, *Valve (瓶阀)*, *Airtightness (气密)*, etc.
    -   **Integrated Uploads**: "Original Record/Field Photo" upload zones are embedded *within* their respective tabs (at the bottom), rather than a separate isolated tab.
    -   **Safety Valve Specialization (Online vs. Offline)**:
        -   **State Management**: `valveType` ('online' | 'offline') controls the UI.
        -   **Mutual Exclusivity**: Switching modes clears/hides irrelevant fields.
        -   **Offline**: Includes "Disassembly" and "Maintenance" fields.
        -   **Online**: Focuses on "In-situ" calibration fields.
    -   **Responsiveness**: Grid system (`el-col`) adapts layout for different screen widths.
