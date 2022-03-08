.class public Lcom/example/x08part2/MainActivity;
.super Landroidx/appcompat/app/AppCompatActivity;
.source "MainActivity.java"


# direct methods
.method public constructor <init>()V
    .locals 0

    .line 7
    invoke-direct {p0}, Landroidx/appcompat/app/AppCompatActivity;-><init>()V

    return-void
.end method


# virtual methods
.method public fun(I)I
    .locals 4
    .param p1, "n"    # I

    .line 18
    const/4 v0, 0x0

    .local v0, "i":I
    const/4 v1, 0x0

    .line 19
    .local v1, "j":I
    const/4 v2, 0x0

    .line 20
    .local v2, "tmp":I
    const/4 v0, 0x0

    :goto_0
    if-ge v0, p1, :cond_1

    .line 21
    const/4 v1, 0x0

    :goto_1
    if-ge v1, p1, :cond_0

    .line 22
    add-int/2addr v2, v1

    .line 23
    const-string v3, "WORLD"

    invoke-static {v3, v3}, Landroid/util/Log;->v(Ljava/lang/String;Ljava/lang/String;)I

    .line 21
    add-int/lit8 v1, v1, 0x1

    goto :goto_1

    .line 20
    :cond_0
    add-int/lit8 v0, v0, 0x1

    goto :goto_0

    .line 26
    :cond_1
    return v2
.end method

.method protected onCreate(Landroid/os/Bundle;)V
    .locals 3
    .param p1, "savedInstanceState"    # Landroid/os/Bundle;

    .line 11
    const/16 v0, 0xa

    invoke-virtual {p0, v0}, Lcom/example/x08part2/MainActivity;->fun(I)I

    move-result v0

    .line 12
    .local v0, "i":I
    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "value: "

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    const-string v2, "MYINT"

    invoke-static {v2, v1}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I

    .line 13
    invoke-super {p0, p1}, Landroidx/appcompat/app/AppCompatActivity;->onCreate(Landroid/os/Bundle;)V

    .line 14
    const v1, 0x7f0b001c

    invoke-virtual {p0, v1}, Lcom/example/x08part2/MainActivity;->setContentView(I)V

    .line 15
    return-void
.end method
