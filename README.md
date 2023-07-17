# Monthly_report
## configure DashBoard with streamlit and Dash
1. [Streamlit version](#streamlit)

2. [Dash version](#dash)

3. [Monthly report prototype](#monthly-report-prototype)

## Streamlit

<details>
<summary>show more</summary>

<!-- summary 아래 한칸 공백 두어야함 -->
<img width="100%" alt="스크린샷 2022-12-02 오후 4 49 24" src="https://user-images.githubusercontent.com/102535447/205242814-e420b949-663e-432f-b93c-1628888462ce.png">
<img width="100%" alt="스크린샷 2022-12-02 오후 4 49 55" src="https://user-images.githubusercontent.com/102535447/205242819-a5041875-f4a0-4f25-984e-b40e1a34dbb3.png">
</details>

## Dash
<details>
<summary>show more</summary>

<!-- summary 아래 한칸 공백 두어야함 -->
<img width="100%" alt="스크린샷 2022-12-02 오후 4 53 07" src="https://user-images.githubusercontent.com/102535447/205243543-1f42a449-f1be-4c80-8b69-0c5a44b89963.png">
<img width="100%" alt="스크린샷 2022-12-02 오후 4 53 29" src="https://user-images.githubusercontent.com/102535447/205243551-2ec906e5-d419-4ceb-b388-805b2c892553.png">
<img width="100%" alt="스크린샷 2022-12-02 오후 4 53 42" src="https://user-images.githubusercontent.com/102535447/205243555-d04100f6-c59a-4a46-8914-7c006e2d4d04.png">
<img width="100%" alt="스크린샷 2022-12-02 오후 4 53 48" src="https://user-images.githubusercontent.com/102535447/205243568-424c7244-3896-4c03-af80-7dcac9963325.png">
<img width="100%" alt="스크린샷 2022-12-02 오후 4 54 06" src="https://user-images.githubusercontent.com/102535447/205243573-9a984b97-9320-4855-b1ef-4e4f6afb3b7d.png">
<img width="100%" alt="스크린샷 2022-12-02 오후 4 54 44" src="https://user-images.githubusercontent.com/102535447/205243593-f13352c3-1fb7-4518-89b9-1ffd242df96b.png">
</details>


## Monthly report prototype

[Dash prototype link](http://15.165.236.197:8050/)

<img width="1624" alt="스크린샷 2022-12-21 오전 11 03 00" src="https://user-images.githubusercontent.com/102535447/208803165-0dcbd75a-b6f0-41f7-ad70-3cf57774670a.png">
* heatmap click 시 해당시간대의 제작 모델 번호, 건강도 display
* 오른쪽 위의 건강도 bar 클릭시 해당 시간의 cycle dedail display

### Heatmap Description
* 건강도 : 금형 Cycle 별로 DWT를 계산하여 오차가 클수록 건강도가 큼(나쁨).
<img width="846" alt="image" src="https://github.com/by-hwa/Monthly_Report/assets/102535447/96a6bb21-5f64-495a-9d1d-b7222e257e41">

* 건강도 측정 알고리즘.
<img width="921" alt="image" src="https://github.com/by-hwa/Monthly_Report/assets/102535447/3bab4ee1-4c35-4ee9-87b6-88edfacd0f2c">
